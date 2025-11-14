# -*- coding: utf-8 -*-
"""
build_perc_bank.py — construct a WORLD template bank for percussion / drums.

This script reads the processed percussion WAV files in assets/perc_wav,
runs WORLD to obtain average spectral envelopes, and stores a small set
of templates in templates/perc_bank.npz.

Because hand percussion often does not have a clear harmonic f0, we
assign artificial "pseudo-f0" values to each template, increasing from
high to low. During conversion, frames with higher f0 will prefer the
"high drum" templates and low f0 frames will prefer the "low drum"
templates.
"""

from pathlib import Path

import numpy as np
import soundfile as sf
import librosa
import pyworld as pw


ROOT = Path(__file__).resolve().parent.parent
WAV_DIR = ROOT / "assets" / "perc_wav"
OUT_NPZ = ROOT / "templates" / "perc_bank.npz"

TARGET_SR = 44100
FRAME_PERIOD_MS = 2.5
F0_FLOOR = 60.0
F0_CEIL = 1200.0


def world_sp_from_noise_like(y: np.ndarray, sr: int):
    """
    Estimate a spectral envelope for a percussion sample using WORLD.

    We use dio only to obtain the frame positions t, then force the f0
    track to a constant value (e.g. 200 Hz) so that cheaptrick can run.
    The mean spectral envelope over time is returned.
    """
    y64 = y.astype(np.float64)
    f0_raw, t = pw.dio(
        y64,
        sr,
        f0_floor=F0_FLOOR,
        f0_ceil=F0_CEIL,
        frame_period=FRAME_PERIOD_MS,
    )
    # Force a constant f0 just for the purpose of cheaptrick
    f0_used = np.full_like(f0_raw, 200.0, dtype=np.float64)
    sp = pw.cheaptrick(y64, f0_used, t, sr)
    return sp.astype(np.float32)


def main() -> None:
    if not WAV_DIR.exists():
        raise FileNotFoundError(f"WAV_DIR does not exist: {WAV_DIR}")

    files = sorted(WAV_DIR.glob("perc_*.wav"))
    if not files:
        print("No perc_*.wav files found in", WAV_DIR)
        return

    f0_list = []
    logsp_list = []
    sr_ref = TARGET_SR
    fftbins_ref = None

    base_f0 = 200.0
    step_f0 = 40.0  # pseudo-f0 spacing between templates

    for idx, p in enumerate(files, start=1):
        print("Analysing percussion sample:", p.name)
        y, sr = sf.read(str(p))
        if y.ndim == 2:
            y = y.mean(axis=1)
        if sr != TARGET_SR:
            y = librosa.resample(y, orig_sr=sr, target_sr=TARGET_SR)
            sr = TARGET_SR
        y = y.astype(np.float32)

        sp = world_sp_from_noise_like(y, sr)
        T, F = sp.shape

        if fftbins_ref is None:
            fftbins_ref = F
        else:
            if F != fftbins_ref:
                print(
                    f"  skip {p.name}: fftbins mismatch (F={F}, expected {fftbins_ref})"
                )
                continue

        sp_mean = np.mean(sp, axis=0)
        logsp = np.log(np.maximum(sp_mean, 1e-12))

        f0_mean = base_f0 + step_f0 * (idx - 1)
        f0_list.append(float(f0_mean))
        logsp_list.append(logsp)

        print(f"  OK: pseudo f0≈{f0_mean:.1f} Hz")

    if not f0_list:
        print("No valid percussion templates were constructed.")
        return

    f0_arr = np.array(f0_list, dtype=float)
    logsp_arr = np.vstack(logsp_list).astype(float)

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

    print("Saved percussion bank ->", OUT_NPZ, f"(N={len(f0_arr)})")


if __name__ == "__main__":
    main()
