# -*- coding: utf-8 -*-
"""
build_violin_bank.py — Constructing violin sound templates from monophonic libraries (WORLD)
"""

from pathlib import Path
import re
import numpy as np
import soundfile as sf
import pyworld as pw
import librosa

ROOT = Path(__file__).resolve().parent.parent
WAV_DIR = ROOT / "assets" / "iowa_wav"      # The pre-processed mono WAV file is placed here.
OUT_NPZ = ROOT / "templates" / "violin_bank.npz"

TARGET_SR = 44100
FRAME_PERIOD_MS = 2.5
F0_FLOOR = 80.0
F0_CEIL = 2000.0

NOTE_RE = re.compile(r'violin_([A-G](?:b|#)?\d)\.wav', re.IGNORECASE)


def world_analysis_single(y: np.ndarray, sr: int):
    """Perform a WORLD analysis on the monophonic sound."""
    y64 = y.astype(np.float64)
    f0, t = pw.dio(
        y64, sr,
        f0_floor=F0_FLOOR,
        f0_ceil=F0_CEIL,
        frame_period=FRAME_PERIOD_MS,
    )
    f0 = pw.stonemask(y64, f0, t, sr)
    sp = pw.cheaptrick(y64, f0, t, sr)
    return f0.astype(np.float32), sp.astype(np.float32)


def pick_steady_region(f0: np.ndarray):
    """
    Simply select the index range for the 'stable portion':
    - Discard the first 10% and last 10% of frames (onsets and offsets)
    - Retain frames within the middle 80% where f0 > 0
    """
    T = len(f0)
    if T < 10:
        return np.ones(T, dtype=bool)
    start = int(T * 0.1)
    end = int(T * 0.9)
    mask = np.zeros(T, dtype=bool)
    mask[start:end] = f0[start:end] > 0
    if not np.any(mask):
        mask[:] = f0 > 0
    if not np.any(mask):
        mask[:] = True
    return mask


def main():
    if not WAV_DIR.exists():
        raise FileNotFoundError(f"WAV_DIR does not exist: {WAV_DIR}，Please run first prepare_iowa_violin.py")

    f0_list = []
    logsp_list = []
    sr_ref = None
    fftbins_ref = None

    files = sorted(WAV_DIR.glob("violin_*.wav"))
    if not files:
        print( WAV_DIR, "No violin_*.wav file was found below.")
        return

    for p in files:
        print("Analyse monophonic sound:", p.name)
        y, sr = sf.read(str(p))
        if y.ndim == 2:
            y = y.mean(axis=1)
        if sr != TARGET_SR:
            y = librosa.resample(y, orig_sr=sr, target_sr=TARGET_SR)
            sr = TARGET_SR
        y = y.astype(np.float32)

        f0, sp = world_analysis_single(y, sr)
        T, F = sp.shape

        if sr_ref is None:
            sr_ref = sr
            fftbins_ref = F
        else:
            if sr != sr_ref or F != fftbins_ref:
                print(f"  Skip {p.name}: sr/fftbins Incompatible (sr={sr}, F={F}, expectation sr={sr_ref}, F={fftbins_ref})")
                continue

        mask = pick_steady_region(f0)
        if not np.any(mask):
            print("  Warning：", p.name, "No stable audio frame detected; skipping.")
            continue

        f0_valid = f0[mask]
        sp_valid = sp[mask, :]

        f0_mean = float(np.median(f0_valid))
        sp_mean = np.mean(sp_valid, axis=0)  # (F,)

        if not np.isfinite(f0_mean) or f0_mean <= 0:
            print("  f0_mean 无效，跳过", p.name)
            continue

        f0_list.append(f0_mean)
        logsp_list.append(np.log(np.maximum(sp_mean, 1e-12)))

        print(f"  OK: f0≈{f0_mean:.1f} Hz")

    if not f0_list:
        print("No templates were successfully constructed. Please check the monophonic files.")
        return

    f0_arr = np.array(f0_list, dtype=float)
    logsp_arr = np.vstack(logsp_list).astype(float)  # (K,F)

    # Sort in ascending order by f0
    order = np.argsort(f0_arr)
    f0_arr = f0_arr[order]
    logsp_arr = logsp_arr[order, :]

    OUT_NPZ.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        OUT_NPZ,
        sr=int(sr_ref),
        fftbins=int(fftbins_ref),
        f0=f0_arr,
        logsp=logsp_arr,
    )

    print("Saved violin bank ->", OUT_NPZ, f"(N={len(f0_arr)})")


if __name__ == "__main__":
    main()
