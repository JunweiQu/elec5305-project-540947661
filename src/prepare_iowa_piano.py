# -*- coding: utf-8 -*-
"""
prepare_iowa_piano.py — pre-process Iowa piano single notes.

This script converts the original Iowa MIS piano recordings (AIFF/WAV) in
assets/piano_raw into normalised mono WAV files at 44.1 kHz in
assets/piano_wav, with consistent file names such as

    piano_C4.wav, piano_Db4.wav, ...

Usage
-----
Place the downloaded piano single-note files (e.g. Piano.mf.C4.aiff) into
assets/piano_raw, then run:

    python src/prepare_iowa_piano.py
"""

from pathlib import Path
import re

import numpy as np
import soundfile as sf
import librosa


ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "assets" / "piano_raw"
WAV_DIR = ROOT / "assets" / "piano_wav"
SR = 44100

# Extract note name from file name, e.g. "Piano.mf.C4.aiff" -> "C4"
NOTE_RE = re.compile(r'([A-G](?:b|#)?\d)', re.IGNORECASE)


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
    for p in files:
        try:
            y, sr = sf.read(str(p))
            if y.ndim == 2:
                y = y.mean(axis=1)
            if sr != SR:
                y = librosa.resample(y, orig_sr=sr, target_sr=SR)
            y = norm_peak(y)

            m = NOTE_RE.search(p.name)
            note = m.group(1).upper() if m else "UNK"
            out = WAV_DIR / f"piano_{note}.wav"
            sf.write(str(out), y, SR)
            kept += 1
            print("OK ->", out.name, "(from", p.name + ")")
        except Exception as e:  # debug print if any sample fails
            print("skip", p.name, ":", e)

    print("total kept:", kept)


if __name__ == "__main__":
    main()
