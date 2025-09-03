# Timbre Transfer via Traditional DSP (Route B) — ELEC5305 Project Proposal

**Goal**  
Change the *timbre* of a **monophonic** input to **piano / violin / erhu** while preserving melody (F0), rhythm and loudness contour.

**Method (Design Only at Proposal Stage)**  
- Analysis: F0 tracking (pYIN/CREPE) + STFT; spectral envelope via cepstral/LPC (WORLD/CheapTrick as reference).  
- Decomposition: Harmonic + Noise (SMS/HNM).  
- Mapping: Envelope replacement conditioned on F0  
  \|Y(ω,t)\| = \|X(ω,t)\| · E_target(ω|F0(t)) / (E_source(ω|F0(t))+ε)  
- Synthesis: iSTFT/OLA; optional PSOLA in voiced segments; loudness matching.

**Evaluation Plan**  
Objective: F0 RMSE, Log-Spectral Distance (LSD) / MFCC distance.  
Subjective: ABX / MUSHRA (ITU-R BS.1534-3).  
Visuals: mel-spectrograms, F0/loudness curves, harmonic–noise energy.

**References (APA 7)**  
Morise, M., Yokomori, F., & Ozawa, K. (2016). WORLD: A vocoder-based high-quality speech synthesis system for real-time applications. *IEICE Transactions on Information and Systems, E99-D*(7), 1877–1884.  
Morise, M. (2015). CheapTrick: A spectral envelope estimator for high-quality speech synthesis. *Speech Communication, 67*, 1–12.  
Serra, X., & Smith, J. O. (1990). Spectral modeling synthesis: Deterministic plus stochastic decomposition. *Computer Music Journal, 14*(4), 12–24.  
Mauch, M., & Dixon, S. (2014). pYIN: A fundamental frequency estimator using probabilistic threshold distributions. In *ICASSP 2014*.  
Kim, J. W., Salamon, J., Li, P., & Bello, J. P. (2018). CREPE: A convolutional representation for pitch estimation. In *ICASSP 2018*.  
ITU-R. (2015). *BS.1534-3: Method for the subjective assessment of intermediate quality level of audio systems (MUSHRA)*.  
Magenta Team. (2017). NSynth dataset (CC BY 4.0).  
Li, B., Liu, X., Dinesh, K., Duan, Z., & Sharma, G. (2019). URMP dataset paper. *IEEE Transactions on Multimedia, 21*(2), 522–535.

**Milestones**  
W1: templates & repository  
W2: analysis module draft  
W3: mapping + synthesis design & objective metrics script  
W4: pilot examples & listening form; iterate based on teaching-staff feedback
