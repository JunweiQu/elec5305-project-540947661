# -*- coding: utf-8 -*-
"""
prepare_iowa_violin.py — Preprocess Iowa violin monophonic samples (supports .wav / .aif)
"""

from pathlib import Path
import re
import numpy as np
import soundfile as sf
import librosa

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR  = ROOT / "assets" / "iowa_raw"
WAV_DIR  = ROOT / "assets" / "iowa_wav"
SR       = 44100  # A sampling rate that works well with WORLD

# Extract the note name from the filename, e.g. "Violin.arco.ff.sulG.G3.stereo.aif" → "G3"
NOTE_RE = re.compile(r'([A-G](?:b|#)?\d)', re.IGNORECASE)


def norm_peak(y: np.ndarray) -> np.ndarray:
    """Peak values are normalised to the range [-0.98, 0.98]."""
    y = np.asarray(y, dtype=np.float32)
    m = float(np.max(np.abs(y)) + 1e-9)
    y = y / m * 0.98
    return y.astype(np.float32)


def main():
    if not RAW_DIR.exists():
        raise FileNotFoundError(f"RAW_DIR does not exist: {RAW_DIR}，Please extract the original violin single notes to this location.")

    WAV_DIR.mkdir(parents=True, exist_ok=True)

    # Supports wav / aif / aiff (case-insensitive)
    exts = ("*.wav", "*.WAV", "*.aif", "*.AIF", "*.aiff", "*.AIFF")
    files = []
    for ext in exts:
        files.extend(RAW_DIR.glob(ext))

    files = sorted(files)
    if not files:
        print( RAW_DIR, "No .wav/.aif files were found below. Please verify that the extraction location is correct.")
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
            note = m.group(1) if m else "UNK"
            out = WAV_DIR / f"violin_{note}.wav"
            sf.write(str(out), y, SR)
            kept += 1
            print("OK ->", out.name)
        except Exception as e:
            print("skip", p.name, ":", e)

    print("total kept:", kept)


if __name__ == "__main__":
    main()
