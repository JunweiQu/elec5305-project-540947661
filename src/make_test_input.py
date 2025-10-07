from pathlib import Path
import numpy as np, soundfile as sf

# Project root directory = one level up from the directory where this script is located
ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "input_demo.wav"

sr = 16000
t = np.linspace(0, 15, 15*sr, endpoint=False)

# A simple fundamental tone track with a slight trill + a small amount of second harmonics + minimal noise
f0 = 220 + 20*np.sin(2*np.pi*0.8*t)
phase = 2*np.pi*np.cumsum(f0)/sr
y = 0.7*np.sin(phase) + 0.2*np.sin(2*phase) + 0.01*np.random.randn(len(t))

y = (y/np.max(np.abs(y))).astype(np.float32)
sf.write(str(OUT_PATH), y, sr)
print("Wrote:", OUT_PATH)
