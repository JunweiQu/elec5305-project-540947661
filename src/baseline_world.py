from pathlib import Path
import numpy as np, librosa, soundfile as sf
import pyworld as pw

# Path: Use absolute paths to avoid "file not found".
ROOT = Path(__file__).resolve().parent.parent
IN_WAV = ROOT / "assets" / "input_demo.wav"
OUT_DIR = ROOT / "reports" / "audio"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_WAV = OUT_DIR / "recon_world.wav"

def world_analysis(y, sr):
    # F0: DIO + StoneMask；Spectral envelope: CheapTrick; acyclic component: D4C
    _f0, t = pw.dio(y.astype(np.float64), sr, f0_floor=50, f0_ceil=1000)
    f0 = pw.stonemask(y.astype(np.float64), _f0, t, sr)
    sp = pw.cheaptrick(y.astype(np.float64), f0, t, sr)   # (frames, freq_bins)
    ap = pw.d4c(y.astype(np.float64), f0, t, sr)          # (frames, freq_bins)
    return f0, t, sp, ap

def world_synthesize(f0, sp, ap, sr):
    y = pw.synthesize(f0, sp, ap, sr)
    y = y / (np.max(np.abs(y)) + 1e-8)
    return y.astype(np.float32)

if __name__ == "__main__":
    assert IN_WAV.exists(), f"Input not found: {IN_WAV}"
    y, sr = librosa.load(str(IN_WAV), sr=16000, mono=True)
    f0, t, sp, ap = world_analysis(y, sr)
    y_rec = world_synthesize(f0, sp, ap, sr)
    sf.write(str(OUT_WAV), y_rec, sr)
    print("OK ->", OUT_WAV)
