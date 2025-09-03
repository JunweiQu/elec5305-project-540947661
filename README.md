# Timbre Transfer via Traditional DSP  — ELEC5305 Project Proposal

**Goal / 目标**  
Change the *timbre* of a **monophonic** input to **piano / violin / erhu** while preserving melody (F0), rhythm, and loudness contour.  
在不改变旋律(F0)、节奏与响度轮廓的前提下，将单旋律音频转换为钢琴/小提琴/二胡音色。

**Method (Design Only at Proposal Stage) / 方法设计（本次仅设计）**  
- Analysis: F0 tracking (pYIN/CREPE) + STFT; spectral envelope via cepstral/LPC（参考 WORLD/CheapTrick）。  
- Decomposition: Harmonic + Noise（SMS/HNM）。  
- Mapping: Envelope replacement conditioned on F0  
  \|Y(ω,t)\| = \|X(ω,t)\| · E_target(ω|F0(t)) / (E_source(ω|F0(t))+ε)  
- Synthesis: iSTFT/OLA（可选 PSOLA 处理有声段）；响度匹配。

**Evaluation Plan / 评测**  
Objective: F0 RMSE, Log-Spectral Distance (LSD) / MFCC distance.  
Subjective: ABX / MUSHRA (ITU-R BS.1534-3)。  
可视化：梅尔谱图、F0/响度曲线、谐波–噪声能量。

**References (APA 7)**  
Morise, M., Yokomori, F., & Ozawa, K. (2016). WORLD... *IEICE E99-D*(7), 1877–1884.  
Morise, M. (2015). CheapTrick... *Speech Communication, 67*, 1–12.  
Serra, X., & Smith, J. O. (1990). Spectral modeling synthesis... *Computer Music Journal, 14*(4), 12–24.  
Mauch, M., & Dixon, S. (2014). pYIN... *ICASSP 2014*.  
Kim, J. W., Salamon, J., Li, P., & Bello, J. P. (2018). CREPE... *ICASSP 2018*.  
ITU-R. (2015). BS.1534-3 (MUSHRA).  
Magenta Team. (2017). NSynth dataset (CC BY 4.0).  
Li, B., Liu, X., Dinesh, K., Duan, Z., & Sharma, G. (2019). URMP... *IEEE TMM, 21*(2), 522–535.

**Milestones / 里程碑**  
W1 模板与仓库；W2 分析模块草案；W3 映射+合成设计与客观指标脚本；W4 小样例与表单，按教学组反馈迭代。
# 5305lab
