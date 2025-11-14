# -*- coding: utf-8 -*-
"""
prepare_iowa_perc.py — pre-process Iowa hand-percussion / woodblock notes.

This script converts the original Iowa percussion recordings in
assets/perc_raw into normalised mono WAV files at 44.1 kHz in
assets/perc_wav, named as

    perc_1.wav, perc_2.wav, ...

Usage
-----
Place the downloaded woodblock / triangle etc. AIFF files into
assets/perc_raw, then run:

    python src/prepare_iowa_perc.py
"""

from pathlib import Path

import numpy as np
import soundfile as sf
import librosa


ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "assets" / "perc_raw"
WAV_DIR = ROOT / "assets" / "perc_wav"
SR = 44100


def norm_peak(y: np.ndarray) -> np.ndarray:
    """Peak-normalise the signal to [-0.98, 0.98]."""
    y = np.asarray(y, dtype=np.float32)
    m = float(np.max(np.abs(y)) + 1e-9)
    y = y / m * 0.98
    return y.astype(np.float32)


def main() -> None:
    if not RAW_DIR.exists():
        raise FileNotFoundError(f"RAW_DIR does not exist: {RAW_DIR}")

    WAV_DIR.mkdir(parents=True, exist_ok=True)

    exts = ("*.wav", "*.WAV", "*.aif", "*.AIF", "*.aiff", "*.AIFF")
    files = []
    for ext in exts:
        files.extend(RAW_DIR.glob(ext))

    files = sorted(files)
    if not files:
        print("No .wav/.aif files found in", RAW_DIR)
        return

    kept = 0
    for idx, p in enumerate(files, start=1):
        try:
            y, sr = sf.read(str(p))
            if y.ndim == 2:
                y = y.mean(axis=1)
            if sr != SR:
                y = librosa.resample(y, orig_sr=sr, target_sr=SR)
            y = norm_peak(y)

            out = WAV_DIR / f"perc_{idx}.wav"
            sf.write(str(out), y, SR)
            kept += 1
            print(f"OK -> {out.name} (from {p.name})")
        except Exception as e:  # debug print if any sample fails
            print("skip", p.name, ":", e)

    print("total kept:", kept)


if __name__ == "__main__":
    main()
