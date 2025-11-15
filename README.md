# Offline Timbre Transfer with WORLD & Iowa Single-Note Banks

ELEC5305 Project – Junwei Qu (SID 540947661)  
School of Electrical and Information Engineering, The University of Sydney

This repository contains my final ELEC5305 project: an **offline timbre transfer tool** for musical audio.  
Given a monophonic WAV file (e.g. a piano recording), the system analyses the signal using the **WORLD vocoder**, then re-synthesises it so that it sounds like being played by a different instrument.

The current prototype supports three target timbres:

- 🎻 Violin (bowed strings)  
- 🎹 Piano  
- 🥁 Drum / percussion

Timbre statistics are learned from **single-note recordings** in the University of Iowa MIS instrument database, and stored in compact spectral “banks”. The project includes both:

- a **research command-line interface** (CLI) that exposes all intermediate steps, and  
- a simple **offline GUI application** (Tkinter, packaged as a Windows `.exe` on my local machine).

---

## 1. Research Question & Motivation

> **Research question:**  
> Can a classical vocoder-based pipeline (WORLD analysis–synthesis + single-note spectral banks) perform practical **instrument timbre transfer** on real music recordings, while preserving melody and timing?

Modern neural style-transfer methods require large training datasets and GPU resources.  
Here I explore a complementary, **light-weight signal-processing approach** that can run fully offline on a laptop, reusing an existing source recording and a small single-note sample set.

The tool is intended for **exploration and education** rather than commercial music production. It allows students to:

- Listen to how **spectral envelope** and **aperiodicity** affect perceived timbre;
- Compare the original WORLD reconstruction (`recon_world.wav`) with timbre-transferred versions (`demo_violin.wav`, `demo_piano.wav`, `demo_drum.wav`);
- Inspect simple quantitative metrics for spectral change.

---

## 2. Repository Structure

The most important files and directories are:

```text
elec5305-project-540947661/
├─ assets/                 # Input audio & raw single-note datasets (not fully tracked in git)
│  ├─ piano_canon.wav      # Example input melody used in the experiments
│  ├─ iowa_raw/            # Raw violin AIF files from Iowa MIS (git-ignored)
│  ├─ iowa_wav/            # Preprocessed violin WAVs (generated)
│  ├─ piano_raw/           # Raw piano AIF files (git-ignored)
│  ├─ piano_wav/           # Preprocessed piano WAVs (generated)
│  ├─ perc_raw/            # Raw hand-percussion AIF files (git-ignored)
│  └─ perc_wav/            # Preprocessed percussion WAVs (generated)
│
├─ docs/
│  ├─ audio/               # Example audio for the project website
│  └─ index.md             # Project web page (GitHub Pages)
│
├─ reports/
│  └─ audio/
│     ├─ recon_world.wav   # WORLD reconstruction of the input (baseline)
│     ├─ demo_violin.wav   # Timbre-transferred output: violin
│     ├─ demo_piano.wav    # Timbre-transferred output: piano
│     └─ demo_drum.wav     # Timbre-transferred output: drum / percussion
│
├─ src/
│  ├─ baseline_world.py    # Core WORLD analysis–synthesis and timbre transfer logic
│  ├─ prepare_input.py     # Down-mix, resample and normalise arbitrary input WAVs
│  ├─ make_test_input.py   # Optional: generate synthetic test tones / melodies
│  │
│  ├─ prepare_iowa_violin.py  # Convert Iowa violin AIF files -> normalised WAVs
│  ├─ prepare_iowa_piano.py   # Convert Iowa piano AIF files -> normalised WAVs
│  ├─ prepare_iowa_perc.py    # Convert Iowa percussion AIF files -> normalised WAVs
│  │
│  ├─ build_violin_bank.py # Build spectral envelope bank for violin
│  ├─ build_piano_bank.py  # Build spectral envelope bank for piano
│  ├─ build_perc_bank.py   # Build spectral envelope bank for percussion
│  │
│  ├─ timbre_app_cli.py    # Research CLI application (main entry point)
│  ├─ timbre_app_gui.py    # Tkinter GUI used for the offline .exe
│  ├─ timbre_app_simple.py # Minimal prototype used in early debugging
│  │
│  ├─ check_levels.py      # Sanity check: sample rate and peak / mean levels
│  └─ metrics_quick.py     # Simple spectral-change metrics for evaluation
│
├─ templates/
│  ├─ violin_bank.npz      # Learned violin spectral bank (generated)
│  ├─ piano_bank.npz       # Learned piano spectral bank (generated)
│  └─ perc_bank.npz        # Learned percussion spectral bank (generated)
│
├─ requirements.txt
└─ README.md
