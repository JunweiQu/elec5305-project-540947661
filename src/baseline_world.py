# -*- coding: utf-8 -*-
"""
baseline_world.py — WORLD vocoder + single-note template banks for timbre transfer.

Supported target timbres:
  - violin : Iowa violin bank
  - piano  : Iowa piano bank
  - drum   : hand-percussion / woodblock bank

This module provides a single high-level function:

    run_world(input_wav: Path | None, target: str) -> None

which analyses the input audio with WORLD, optionally applies a
timbre-transfer step using a template bank, and writes the outputs
into reports/audio/.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import soundfile as sf
import librosa
import pyworld as pw


# -----------------------------------------------------------------------------
# Paths and global settings
# -----------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"
TEMPLATES_DIR = ROOT / "templates"
OUT_DIR = ROOT / "reports" / "audio"

OUT_DIR.mkdir(parents=True, exist_ok=True)

IN_WAV_DEFAULT = ASSETS_DIR / "input_demo.wav"

VIOLIN_BANK_PATH = TEMPLATES_DIR / "violin_bank.npz"
PIANO_BANK_PATH = TEMPLATES_DIR / "piano_bank.npz"
PERC_BANK_PATH = TEMPLATES_DIR / "perc_bank.npz"

TARGET_SR = 44100
FRAME_PERIOD_MS = 2.5
F0_FLOOR = 60.0
F0_CEIL = 900.0

# Blend factors for different target timbres.
# alpha = 0.0  -> keep original timbre
# alpha = 1.0  -> use template timbre only
BLEND_MAP = {
    "violin": 0.8,
    "piano": 0.4,
    "drum": 1.0,
}


# -----------------------------------------------------------------------------
# f0 post-processing
# -----------------------------------------------------------------------------

def make_continuous_f0(f0: np.ndarray) -> np.ndarray:
    """
    Make the f0 trajectory continuous and slightly smoothed.

    Steps:
      1. Interpolate unvoiced frames (where f0 == 0) using neighbouring
         voiced frames.
      2. Apply a short moving-average filter (length 5) to reduce jitter.
    """
    f0 = f0.astype(np.float64)
    T = len(f0)
    t = np.arange(T)

    voiced = f0 > 0
    if not np.any(voiced):
        # No voiced frames at all – nothing we can do.
        return f0.astype(np.float64)

    t_voiced = t[voiced]
    f0_voiced = f0[voiced]

    # Linear interpolation over unvoiced gaps
    f0_interp = np.interp(t, t_voiced, f0_voiced)

    # Moving-average smoothing
    win = 5
    pad = win // 2
    pad_data = np.pad(f0_interp, (pad, pad), mode="edge")
    kernel = np.ones(win, dtype=np.float64) / win
    smooth = np.convolve(pad_data, kernel, mode="valid")

    return smooth.astype(np.float64)


# -----------------------------------------------------------------------------
# WORLD analysis and synthesis
# -----------------------------------------------------------------------------

def world_analysis(y: np.ndarray, sr: int):
    """
    Run WORLD analysis on a mono signal.

    Returns
    -------
    f0 : np.ndarray, shape (T,)
        Smoothed f0 trajectory in Hz.
    t : np.ndarray, shape (T,)
        Time positions of analysis frames.
    sp : np.ndarray, shape (T, F)
        Spectral envelope from cheaptrick.
    ap : np.ndarray, shape (T, F)
        Aperiodicity from d4c.
    """
    y64 = y.astype(np.float64)

    # Step 1: f0 estimation
    f0_raw, t = pw.harvest(
        y64,
        sr,
        f0_floor=F0_FLOOR,
        f0_ceil=F0_CEIL,
        frame_period=FRAME_PERIOD_MS,
    )
    f0_refined = pw.stonemask(y64, f0_raw, t, sr)

    # Step 2: make f0 continuous and smooth
    f0_smooth = make_continuous_f0(f0_refined)

    # Step 3: spectral envelope and aperiodicity using smoothed f0
    sp = pw.cheaptrick(y64, f0_smooth, t, sr)
    ap = pw.d4c(y64, f0_smooth, t, sr)

    return (
        f0_smooth.astype(np.float32),
        t,
        sp.astype(np.float32),
        ap.astype(np.float32),
    )


def world_synthesize(
    f0: np.ndarray,
    sp: np.ndarray,
    ap: np.ndarray,
    sr: int,
    frame_ms: float = FRAME_PERIOD_MS,
) -> np.ndarray:
    """
    WORLD synthesis helper.

    Slightly reduces the aperiodic component to avoid overly noisy output,
    and peak-normalises the result to a maximum absolute value of 0.98.
    """
    # Reduce aperiodicity a little bit: 0 = fully periodic, 1 = fully noise.
    ap2 = np.clip(ap * 0.8, 0.0, 1.0)

    y = pw.synthesize(
        f0.astype(np.float64),
        sp.astype(np.float64),
        ap2.astype(np.float64),
        sr,
        frame_period=frame_ms,
    ).astype(np.float32)

    # Replace NaNs/Infs by zeros
    y = np.nan_to_num(y, nan=0.0, posinf=0.0, neginf=0.0)

    max_abs = float(np.max(np.abs(y)))
    if max_abs > 0:
        y = y / max_abs * 0.98

    return y.astype(np.float32)


# -----------------------------------------------------------------------------
# Template bank utilities
# -----------------------------------------------------------------------------

def load_bank(path: Path):
    """
    Load an instrument template bank in npz format.

    The npz file is expected to contain:
      - 'sr'     : sampling rate
      - 'fftbins': number of spectral bins
      - 'f0'     : mean f0 of each template
      - 'logsp'  : log-magnitude spectral envelope for each template
    """
    if not path.exists():
        print(f"[baseline_world] WARNING: bank file not found: {path}")
        return None

    data = np.load(str(path))
    bank = {
        "sr": int(data["sr"]),
        "fftbins": int(data["fftbins"]),
        "f0": data["f0"].astype(float),
        "logsp": data["logsp"].astype(float),
    }
    return bank


def interp_template_logsp_nearest(bank: dict, f0_t: float):
    """
    Pick the nearest template (in f0) from the bank for a given frame f0.

    Returns
    -------
    logsp : np.ndarray, shape (F,) or None
        Log-magnitude spectrum of the selected template, or None if
        the frame is considered unvoiced.
    """
    if f0_t <= 0 or not np.isfinite(f0_t):
        return None
    f0s = bank["f0"]
    idx = int(np.argmin(np.abs(f0s - f0_t)))
    return bank["logsp"][idx]


def apply_timbre_with_blend(
    f0: np.ndarray,
    sp: np.ndarray,
    bank: dict,
    blend: float,
) -> np.ndarray:
    """
    Apply timbre transfer by interpolating between the original spectral
    envelope and a template envelope in the log-spectral domain:

        log|S_out| = (1 - blend) * log|S_orig| + blend * log|S_template|

    A short temporal smoothing filter is applied along the time axis to
    reduce frame-to-frame discontinuities.
    """
    T, F = sp.shape

    logsp_orig = np.log(np.maximum(sp, 1e-12))
    logsp_out = np.zeros((T, F), dtype=np.float64)
    last_tmpl = None

    blend = float(np.clip(blend, 0.0, 1.0))

    for t_idx in range(T):
        f = float(f0[t_idx])
        tmpl_log = interp_template_logsp_nearest(bank, f)

        if tmpl_log is None or not np.all(np.isfinite(tmpl_log)):
            if last_tmpl is not None:
                tmpl_log = last_tmpl
            else:
                tmpl_log = logsp_orig[t_idx]
        else:
            last_tmpl = tmpl_log

        logsp_out[t_idx] = (1.0 - blend) * logsp_orig[t_idx] + blend * tmpl_log

    # Temporal smoothing: 3-frame moving average per frequency bin
    win = 3
    pad = win // 2
    pad_data = np.pad(logsp_out, ((pad, pad), (0, 0)), mode="edge")
    kernel = np.ones(win, dtype=np.float64) / win
    smooth = np.empty_like(logsp_out)
    for f_idx in range(F):
        smooth[:, f_idx] = np.convolve(pad_data[:, f_idx], kernel, mode="valid")

    sp_out = np.exp(smooth).astype(np.float32)
    return sp_out


# -----------------------------------------------------------------------------
# Public API
# -----------------------------------------------------------------------------

def run_world(input_wav: Path | None = None, target: str = "violin") -> None:
    """
    High-level entry point for timbre transfer.

    Parameters
    ----------
    input_wav:
        Path to the input audio file. If None, uses assets/input_demo.wav.
    target:
        Target timbre: one of {"violin", "piano", "drum"}.

    Outputs
    -------
    Always writes a WORLD reconstruction to:
        reports/audio/recon_world.wav

    And a timbre-transferred signal to one of:
        reports/audio/demo_violin.wav
        reports/audio/demo_piano.wav
        reports/audio/demo_drum.wav
    """
    target = target.lower()
    if target not in {"violin", "piano", "drum"}:
        raise ValueError(f"Unknown target timbre: {target}")

    in_wav = Path(input_wav) if input_wav is not None else IN_WAV_DEFAULT
    if not in_wav.exists():
        raise FileNotFoundError(f"Input audio not found: {in_wav}")

    # Load and resample to TARGET_SR
    y, sr_in = sf.read(str(in_wav))
    if y.ndim == 2:
        y = y.mean(axis=1)
    if sr_in != TARGET_SR:
        y = librosa.resample(y, orig_sr=sr_in, target_sr=TARGET_SR)
    y = y.astype(np.float32)
    sr = TARGET_SR

    print(f"[baseline_world] input: {in_wav}, sr_in={sr_in}, len={len(y)}")

    # WORLD analysis
    f0, t_axis, sp, ap = world_analysis(y, sr)
    print(f"[baseline_world] WORLD analysis: frames={sp.shape[0]}, fftbins={sp.shape[1]}")

    # WORLD reconstruction (used as a baseline reference)
    y_rec = world_synthesize(f0, sp, ap, sr)
    out_recon = OUT_DIR / "recon_world.wav"
    sf.write(str(out_recon), y_rec, sr)
    print("[baseline_world] wrote reconstruction:", out_recon)

    # Select the appropriate template bank and output name
    if target == "violin":
        bank_path = VIOLIN_BANK_PATH
        out_demo = OUT_DIR / "demo_violin.wav"
    elif target == "piano":
        bank_path = PIANO_BANK_PATH
        out_demo = OUT_DIR / "demo_piano.wav"
    else:  # "drum"
        bank_path = PERC_BANK_PATH
        out_demo = OUT_DIR / "demo_drum.wav"

    print(f"[baseline_world] target={target}, using bank={bank_path}")

    bank = load_bank(bank_path)
    if bank is None:
        print(f"[baseline_world] Bank not found for target={target}, skipping timbre transfer.")
        return

    if bank["fftbins"] != sp.shape[1]:
        print(
            "[baseline_world] WARNING: bank fftbins do not match analysis fftbins "
            f"({bank['fftbins']} vs {sp.shape[1]}). "
            "Please regenerate the banks with the same WORLD settings."
        )
        return

    blend = BLEND_MAP.get(target, 0.6)
    sp_tgt = apply_timbre_with_blend(f0, sp, bank, blend=blend)
    y_tgt = world_synthesize(f0, sp_tgt, ap, sr)
    sf.write(str(out_demo), y_tgt, sr)
    print(f"[baseline_world] wrote timbre-transfer result ({target}):", out_demo)


def _main_cli() -> None:
    """
    Command-line interface:

        python baseline_world.py [input_wav] [target]

    Examples
    --------
    python baseline_world.py
    python baseline_world.py assets\\piano_canon.wav violin
    python baseline_world.py assets\\piano_canon.wav drum
    """
    args = sys.argv[1:]
    in_wav: Path | None = None
    target = "violin"
    if len(args) >= 1:
        in_wav = Path(args[0])
    if len(args) >= 2:
        target = args[1]
    run_world(in_wav, target)


if __name__ == "__main__":
    _main_cli()
