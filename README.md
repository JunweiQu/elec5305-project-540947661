# Timbre Transfer via Traditional DSP 

**Project status:** proposal stage, initial implementation & testing 
**Project site:** https://junweiqu.github.io/elec5305-project-540947661/  
**Repository:** https://github.com/JunweiQu/elec5305-project-540947661

## Overview
We change the **timbre** of a **monophonic** input to **piano, violin, or erhu** while preserving melody (F0), rhythm, and loudness contour. The focus is an **interpretable DSP pipeline** ): F0 tracking (pYIN/CREPE), STFT-based spectral envelope estimation (cepstral/LPC; WORLD/CheapTrick as reference), harmonic–noise decomposition (SMS/HNM), F0‑conditioned envelope replacement, and iSTFT/OLA resynthesis with optional PSOLA.

## Baselines & Data
- **Baselines (code to start with):** `librosa.pyin`, **CREPE** (pretrained), **LPC/cepstral envelope**, optional **pyworld**.  
- **Exploratory track (requested by teaching staff):** try **DDSP** timbre-transfer baseline for comparison.  
- **Datasets:** **NSynth** (single notes) for envelope templates; **URMP** isolated strings for analysis/validation; curate small erhu sample set (public-domain or permissive license).

## Week 9 progress (checklist)
- [x] Literature review (Route B: WORLD/CheapTrick, SMS/HNM; Route C: DDSP)
- [x] Dataset shortlist (NSynth/URMP; erhu samples to be curated)
- [x] Baseline code setup: pYIN & CREPE working on test clips; STFT + cepstral envelope extraction
- [ ] First envelope-replacement demo (10–20 s) and LSD/MFCC metrics
- [ ] Add ABX/MUSHRA listening form and pilot participants

## Next steps (Weeks 10–11)
- Implement harmonic–noise split and per-branch smoothing; compare LPC vs. cepstral vs. CheapTrick
- Run objective metrics (F0 RMSE, LSD/MFCC); collect ABX/MUSHRA ratings
- Prepare audio demos for **piano/violin/erhu** and finalize plots

## References (APA 7)
Morise, M., Yokomori, F., & Ozawa, K. (2016). WORLD: A vocoder-based high-quality speech synthesis system for real-time applications. *IEICE Transactions on Information and Systems, E99-D*(7), 1877–1884. https://doi.org/10.1587/transinf.2015EDP7457  
Morise, M. (2015). CheapTrick: A spectral envelope estimator for high-quality speech synthesis. *Speech Communication, 67*, 1–7. https://doi.org/10.1016/j.specom.2014.09.003  
Serra, X., & Smith, J. O. (1990). Spectral modeling synthesis: Deterministic plus stochastic decomposition. *Computer Music Journal, 14*(4), 12–24.  
Mauch, M., & Dixon, S. (2014). pYIN: A fundamental frequency estimator using probabilistic threshold distributions. In *ICASSP 2014*, 659–663. https://doi.org/10.1109/ICASSP.2014.6853678  
Kim, J. W., Salamon, J., Li, P., & Bello, J. P. (2018). CREPE: A convolutional representation for pitch estimation. In *ICASSP 2018*, 161–165.  
Engel, J., Hantrakul, L., Gu, C., & Roberts, A. (2020). DDSP: Differentiable digital signal processing. In *ICLR 2020*.  
Li, B., Liu, X., Dinesh, K., Duan, Z., & Sharma, G. (2019). Creating a multitrack classical music performance dataset for multimodal music analysis. *IEEE Transactions on Multimedia, 21*(2), 522–535. https://doi.org/10.1109/TMM.2018.2856090  
Magenta Team. (2017). NSynth dataset (CC BY 4.0). https://magenta.withgoogle.com/datasets/nsynth
