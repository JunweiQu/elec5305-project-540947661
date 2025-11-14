from pathlib import Path
import json, numpy as np, librosa

ROOT = Path(__file__).resolve().parent.parent
SR = 16000
N_FFT, HOP = 2048, 256

def load_mono_16k(p):
    y, sr = librosa.load(str(p), sr=SR, mono=True)
    y = y / (np.max(np.abs(y)) + 1e-8)
    return y

def stft_mag(y):
    S = np.abs(librosa.stft(y, n_fft=N_FFT, hop_length=HOP, win_length=1024))
    return S + 1e-8

def lsd_db(S1, S2):
    T = min(S1.shape[1], S2.shape[1])
    S1, S2 = S1[:, :T], S2[:, :T]
    D = (20*np.log10(S1) - 20*np.log10(S2))**2
    lsd = np.sqrt(np.mean(D, axis=0))     # per-frame
    return float(np.mean(lsd))

def mfcc_dist(y1, y2):
    M1 = librosa.feature.mfcc(y=y1, sr=SR, n_mfcc=20, n_fft=N_FFT, hop_length=HOP)
    M2 = librosa.feature.mfcc(y=y2, sr=SR, n_mfcc=20, n_fft=N_FFT, hop_length=HOP)
    T = min(M1.shape[1], M2.shape[1])
    d = np.linalg.norm(M1[:, :T] - M2[:, :T], axis=0)
    return float(np.mean(d))

def rms(x): return float(np.sqrt(np.mean(x**2)) + 1e-12)
def spec_centroid(y):
    c = librosa.feature.spectral_centroid(y=y, sr=SR, n_fft=N_FFT, hop_length=HOP)
    return float(np.mean(c))

if __name__ == "__main__":
    ref = ROOT / "reports" / "audio" / "recon_world.wav"   # 作为参考（同旋律）
    test = ROOT / "reports" / "audio" / "demo_violin.wav"  # 小提琴转换后

    y_ref = load_mono_16k(ref)
    y_tst = load_mono_16k(test)

    S_ref, S_tst = stft_mag(y_ref), stft_mag(y_tst)
    metrics = {
        "LSD_dB": lsd_db(S_ref, S_tst),                         # 越大差异越明显（谱包络变化）
        "MFCC_L2": mfcc_dist(y_ref, y_tst),                    # MFCC 均值距离
        "RMS_ratio": rms(y_tst) / rms(y_ref),                  # 响度比
        "Centroid_diff_Hz": spec_centroid(y_tst) - spec_centroid(y_ref)
    }
    print(json.dumps(metrics, indent=2))

    out_json = ROOT / "reports" / "metrics.json"
    out_json.write_text(json.dumps(metrics, indent=2))
    print("saved ->", out_json)
