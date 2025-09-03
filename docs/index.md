---
title: ELEC5305 Project Proposal — Timbre Transfer (Route B)
---

## Summary / 项目概述
This project changes the *timbre* of a **monophonic** input to **piano / violin / erhu** while preserving melody (F0), rhythm and loudness contour. It adopts an interpretable DSP pipeline: F0 tracking (pYIN/CREPE), STFT-based spectral envelope estimation (cepstral/LPC; WORLD/CheapTrick as reference), harmonic–noise (SMS/HNM) decomposition, F0-conditioned envelope replacement, and iSTFT/OLA resynthesis with optional PSOLA.

**中文**：在保持旋律(F0)、节奏与响度不变的前提下，将单旋律音频的音色迁移到钢琴/小提琴/二胡。采用可解释的 B 路线（F0→包络→H/N→包络替换→合成），用于课程展示与评测。

## Evaluation / 评测
- Objective: F0 RMSE, Log-Spectral Distance (LSD) / MFCC distance  
- Subjective: ABX / MUSHRA (ITU-R BS.1534-3)  
- Visuals: mel-spectrograms, F0/loudness curves

## References
See the README for APA-style references.

---
GitHub repo: <https://github.com/yourname/elec5305-timbre-transfer>
