# Timbre Transfer via Traditional DSP — ELEC5305 Project Proposal

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

### References (APA 7)
Morise, M., Yokomori, F., & Ozawa, K. (2016). WORLD: A vocoder-based high-quality speech synthesis system for real-time applications. *IEICE Transactions on Information and Systems, E99-D*(7), 1877–1884. https://doi.org/10.1587/transinf.2015EDP7457

Morise, M. (2015). CheapTrick: A spectral envelope estimator for high-quality speech synthesis. *Speech Communication, 67*, 1–7. https://doi.org/10.1016/j.specom.2014.09.003

Serra, X., & Smith, J. O. (1990). Spectral modeling synthesis: Deterministic plus stochastic decomposition. *Computer Music Journal, 14*(4), 12–24. https://www.jstor.org/stable/3680788

Mauch, M., & Dixon, S. (2014). pYIN: A fundamental frequency estimator using probabilistic threshold distributions. In *2014 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)* (pp. 659–663). https://doi.org/10.1109/ICASSP.2014.6853678

Kim, J. W., Salamon, J., Li, P., & Bello, J. P. (2018). CREPE: A convolutional representation for pitch estimation. In *2018 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)* (pp. 161–165). (Open-access preprint: arXiv:1802.06182)

ITU-R. (2015). *BS.1534-3: Method for the subjective assessment of intermediate quality level of audio systems (MUSHRA)*. International Telecommunication Union. (Official page: R-REC-BS.1534-3, 2015-10-14)

Magenta Team. (2017). *NSynth dataset* (CC BY 4.0). https://magenta.withgoogle.com/datasets/nsynth

Li, B., Liu, X., Dinesh, K., Duan, Z., & Sharma, G. (2019). Creating a multitrack classical music performance dataset for multimodal music analysis: Challenges, insights, and applications. *IEEE Transactions on Multimedia, 21*(2), 522–535. https://doi.org/10.1109/TMM.2018.2856090
