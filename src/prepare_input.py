from pathlib import Path
import sys, numpy as np, librosa, soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "input_demo.wav"   # pipeline 固定读取这个

def rms(x): return float(np.sqrt(np.mean(x**2)) + 1e-12)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/prepare_input.py <path_to_audio>")
        raise SystemExit(1)

    src = Path(sys.argv[1])
    y, sr = librosa.load(str(src), sr=44100, mono=True)  # 44.1 kHz

    # 1) 去首尾静音（适度）
    y, _ = librosa.effects.trim(y, top_db=35)

    # 2) 限制时长到 6–12s（太长会拖慢，可按需改）
    max_len = int(12 * 16000)
    if len(y) > max_len:
        y = y[:max_len]

    # 3) 归一化避免削顶
    y = y / (np.max(np.abs(y)) + 1e-8)

    # 4) 写成 pipeline 的标准输入
    sf.write(str(OUT), y.astype(np.float32), 44100)
    print("wrote ->", OUT, "dur(s)=", round(len(y)/44100, 2))
