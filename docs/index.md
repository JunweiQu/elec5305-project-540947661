# Offline Timbre Transfer with WORLD and Iowa Single-Note Banks

ELEC5305 – Speech and Audio Processing  
Author: Junwei Qu (SID 540947661)  
Semester 2, 2025 – The University of Sydney  

---

## 1. Project Overview

This project investigates **instrument timbre transfer** using a classical signal-processing approach rather than a neural network.

Given an input WAV file (for example, a short piano recording), the system:

1. Analyses the audio using the **WORLD vocoder**,  
2. Replaces the spectral envelope with one drawn from a **single-note instrument bank** built from the University of Iowa MIS dataset, and  
3. Re-synthesises the waveform so that it sounds like being played by a different instrument.

The current implementation supports **three target timbres**:

- Violin  
- Piano  
- Drum / percussion  

The repository contains both a **research pipeline** (command-line scripts) and a small **offline GUI application** that demonstrates the effect interactively.

You can find the full code here:  
https://github.com/JunweiQu/elec5305-project-540947661

---

## 2. Research Question and Motivation

**Research question**

> Can a WORLD-based analysis–synthesis pipeline, combined with single-note spectral banks from Iowa MIS, achieve perceptually convincing instrument timbre transfer for monophonic music recordings, without training a deep neural network?

**Motivation**

Recent timbre-transfer research is dominated by deep learning. Such systems are powerful but often difficult to reproduce within a single semester project. In contrast, this work focuses on:

- Transparency – WORLD parameters (F0, spectral envelope, aperiodicity) are interpretable,  
- Simplicity – the whole system runs fully offline on a laptop, and  
- Education – the code can be used as a small case study for audio signal processing in ELEC5305.

---

## 3. Method

### 3.1 Input preparation

- Input audio is expected to be a **mono WAV** file with a standard sampling rate.  
- `prepare_input.py` converts stereo to mono, resamples if necessary and normalises the level.  
- The main example in the experiments is `assets/piano_canon.wav`, a piano excerpt of Canon in D.

### 3.2 Building instrument banks

For each target instrument (violin, piano, percussion), the following steps are carried out:

1. **Pre-processing Iowa MIS recordings**

   - Raw AIF files are placed in `assets/iowa_raw/`, `assets/piano_raw/` and `assets/perc_raw/`.  
   - Scripts `prepare_iowa_violin.py`, `prepare_iowa_piano.py` and `prepare_iowa_perc.py` convert them to cleaned WAVs in corresponding `*_wav` folders.  
   - Silence is trimmed and levels are normalised.

2. **WORLD analysis of single notes**

   - Each cleaned note is analysed by WORLD to obtain time-varying spectral envelopes.

3. **Spectral template aggregation**

   - Envelopes are aligned on a semitone grid and averaged, producing a compact **spectral bank** for each instrument.  
   - The resulting templates are stored as `.npz` files in `templates/`.

### 3.3 Timbre transfer with WORLD

The core algorithm is implemented in `baseline_world.py` and is used by both the CLI and the GUI:

1. Analyse the input with WORLD into F0, spectral envelope and aperiodicity.  
2. Synthesise a **baseline reconstruction** using the original envelope (`recon_world.wav`).  
3. For each frame, look up a template spectral envelope from the chosen bank based on the current F0.  
4. Blend the original and template envelopes with a fixed mixing factor to avoid losing all characteristics of the input.  
5. Re-synthesise the waveform using WORLD, resulting in `demo_violin.wav`, `demo_piano.wav` or `demo_drum.wav`.

---

## 4. Software and Usage

### 4.1 Command-line interface

The main script is:

```bash
python src/timbre_app_cli.py
```

It prompts the user for an input WAV path and a target timbre (violin, piano or drum) and then runs the full pipeline. Outputs are written to `reports/audio/`.

Additional helper scripts:

- `check_levels.py` – prints sample rate and level statistics for sanity checking,  
- `metrics_quick.py` – computes simple spectral-distance measures between baseline and converted signals, and  
- `make_test_input.py` – generates synthetic test tones and melodies.

### 4.2 GUI interface

```bash
python src/timbre_app_gui.py
```

The Tkinter GUI allows a user to:

1. Browse for an input WAV file,  
2. Select a target timbre via radio buttons, and  
3. Click “Run conversion” and follow the log messages.

The GUI calls the same core functions as the CLI and writes output WAVs to `reports/audio/`.  
On my local Windows machine I also built a Windows `.exe` from this script using PyInstaller for offline demonstration.

---

## 5. Experimental Results – High-Level Summary

Experiments were run on three main conversions:

1. **Piano → Violin**  
   - Melody and rhythm are preserved, and the output sounds clearly more like a string instrument.  
   - However, attacks can be too soft and long notes lack realistic expression.

2. **Piano → Piano (self-transfer)**  
   - Confirms that the pipeline does not completely destroy the input when the source and target timbres are similar.  
   - Small spectral differences are still measurable.

3. **Piano → Drum / Percussion**  
   - Produces creative, percussive-sounding textures but not a realistic drum performance.  
   - Demonstrates the limitations of using only harmonic spectral envelopes for strongly percussive sounds.

---

## 6. Conclusions and Future Work

The results show that a **classical WORLD-based pipeline with Iowa spectral banks** can perform meaningful timbre transfer for simple, monophonic music, even without any deep learning. The approach is transparent, easy to reproduce and suitable for teaching.

However, there are clear limitations:

- Performance degrades on polyphonic or highly mixed audio,  
- Expressive details such as dynamics and vibrato are not fully captured, and  
- Percussion remains difficult to model with purely harmonic envelopes.

Future work could integrate harmonic–percussive source separation, adaptive blending schedules, additional instruments from Iowa MIS and comparisons with small neural vocoders or diffusion models.

---

## 7. Audio Examples

The `docs/audio/` folder and the `reports/audio/` folder contain small WAV examples:

- `recon_world.wav` – WORLD reconstruction baseline,  
- `demo_violin.wav` – Piano → violin transfer,  
- `demo_piano.wav` – Piano → piano self-transfer,  
- `demo_drum.wav` – Piano → drum / percussion transfer.

These examples are referenced in the written report and the project video to illustrate the perceptual effect of the proposed method.
