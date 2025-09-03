---
title: ELEC5305 Project Proposal — Timbre Transfer 
---

## Summary 
This project changes the *timbre* of a **monophonic** input to **piano / violin / erhu** while preserving melody (F0), rhythm and loudness contour. It adopts an interpretable DSP pipeline: F0 tracking (pYIN/CREPE), STFT-based spectral envelope estimation (cepstral/LPC; WORLD/CheapTrick as reference), harmonic–noise (SMS/HNM) decomposition, F0-conditioned envelope replacement, and iSTFT/OLA resynthesis with optional PSOLA.

## Evaluation 
- Objective: F0 RMSE, Log-Spectral Distance (LSD) / MFCC distance  
- Subjective: ABX / MUSHRA (ITU-R BS.1534-3)  
- Visuals: mel-spectrograms, F0/loudness curves

## References
See the README for APA-style references.

---
GitHub repo: <https://github.com/yourname/elec5305-timbre-transfer>
