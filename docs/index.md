---
title: ELEC5305 Project Proposal — Timbre Transfer 
---

**Status:** initial implementation & testing.  
**Repo:** <https://github.com/JunweiQu/elec5305-project-540947661>

## Summary
We target **timbre transfer** for **monophonic** inputs to **piano/violin/erhu**, preserving melody (F0), rhythm, and loudness contour. The Route‑B DSP pipeline: F0 (pYIN/CREPE) → STFT + spectral envelope (cepstral/LPC; WORLD/CheapTrick) → SMS/HNM (harmonic–noise) → F0‑conditioned envelope replacement → iSTFT/OLA (+ optional PSOLA).

## Baseline code & datasets
- `librosa.pyin`, **CREPE**, **LPC/cepstral envelope**, optional **pyworld**; exploratory **DDSP** baseline.  
- **NSynth** for envelope templates; **URMP** for isolated strings; small erhu set to be curated (permissive license).

## Week 9 checklist
- Literature review ✓; dataset shortlist ✓; baseline code setup ✓  
- First demo & metrics → in progress; listening form → in progress

## Feedback we seek
- Are the datasets sufficient for piano/violin/erhu coverage?  
- Which envelope estimator (LPC vs. cepstral vs. CheapTrick) would you prefer as primary?  
- Is the DDSP baseline comparison adequate for the scope of ELEC5305?

## References
(See repo README for full APA list.)

## Audio demos

**WORLD re-synthesis**  
<audio controls preload="metadata">
  <source src="{{ site.baseurl }}/audio/recon_world.wav" type="audio/wav">
  Your browser does not support the audio element.
  <a href="{{ site.baseurl }}/audio/recon_world.wav">Download WAV</a>
</audio>

**Violin-converted demo**
<audio controls preload="metadata">
  <source src="{{ site.baseurl }}/audio/demo_violin.wav" type="audio/wav">
  <a href="{{ site.baseurl }}/audio/demo_violin.wav">Download WAV</a>
</audio>


