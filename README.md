# Offline Timbre Transfer with WORLD and Iowa Single-Note Banks

ELEC5305 – Speech and Audio Processing  
Author: Junwei Qu (SID 540947661)  
School of Electrical and Information Engineering, The University of Sydney  

This repository contains my final ELEC5305 project: an **offline timbre transfer tool** for musical audio.  
Given a monophonic WAV file (for example, a short piano performance), the system analyses the signal using the **WORLD vocoder** and then re-synthesises it so that it sounds like being played by a different instrument.

The current prototype supports three target timbres:

- Violin  
- Piano  
- Drum / percussion  

Timbre characteristics are learned from **single-note recordings** in the University of Iowa Musical Instrument Samples (MIS) database and stored in compact spectral “banks”. The project provides both:

- a **research command-line interface (CLI)** that exposes all intermediate steps, and  
- a simple **offline GUI application** (Tkinter), which I also packaged locally as a Windows `.exe`.

---

## 1. Research Question and Motivation

**Research question**

> Can a classical vocoder-based pipeline (WORLD analysis–synthesis plus single-note spectral banks) perform practical **instrument timbre transfer** on real music recordings, while preserving melody and timing and without any deep neural network?

Recent timbre-transfer and style-transfer systems are mostly neural-network based. They can produce impressive results but usually require:

- large training datasets,  
- GPU hardware,  
- complex training and tuning.

In this project I explore a complementary, **light-weight signal-processing approach** that runs fully offline on a laptop. The goals are:

- To study how **spectral envelope** and **aperiodicity** control perceived timbre,  
- To provide a small, reproducible code base for future ELEC5305 students, and  
- To evaluate where a non-neural approach works well and where it clearly fails.

---

## 2. Repository Structure

The most important files and folders are:

- `assets/` – Input audio and raw single-note datasets (large files are ignored by git).  
  - `piano_canon.wav` – Example input melody used in the experiments.  
  - `iowa_raw/` – Raw violin AIF files from Iowa MIS (not tracked).  
  - `iowa_wav/` – Preprocessed violin WAVs (generated).  
  - `piano_raw/` – Raw piano AIF files (not tracked).  
  - `piano_wav/` – Preprocessed piano WAVs (generated).  
  - `perc_raw/` – Raw hand-percussion AIF files (not tracked).  
  - `perc_wav/` – Preprocessed percussion WAVs (generated).

- `docs/` – Project web page for GitHub Pages.  
  - `audio/` – Small example audio files.  
  - `index.md` – Project overview (for the website).

- `reports/audio/` – Output WAV files used in the report and video.  
  - `recon_world.wav` – WORLD reconstruction of the input (baseline).  
  - `demo_violin.wav` – Timbre-transferred output (violin).  
  - `demo_piano.wav` – Timbre-transferred output (piano).  
  - `demo_drum.wav` – Timbre-transferred output (drum / percussion).

- `src/` – All source code.  
  - `baseline_world.py` – Core WORLD analysis–synthesis and timbre-transfer logic.  
  - `prepare_input.py` – Down-mix, resample and normalise arbitrary input WAVs.  
  - `make_test_input.py` – Utility to generate synthetic test tones and melodies.  
  - `prepare_iowa_violin.py` – Convert Iowa violin AIF files → cleaned WAVs.  
  - `prepare_iowa_piano.py` – Convert Iowa piano AIF files → cleaned WAVs.  
  - `prepare_iowa_perc.py` – Convert Iowa percussion AIF files → cleaned WAVs.  
  - `build_violin_bank.py` – Build spectral envelope bank for violin.  
  - `build_piano_bank.py` – Build spectral envelope bank for piano.  
  - `build_perc_bank.py` – Build spectral envelope bank for percussion.  
  - `timbre_app_cli.py` – Research command-line app (main entry point).  
  - `timbre_app_gui.py` – Tkinter GUI used for the offline `.exe`.  
  - `timbre_app_simple.py` – Minimal prototype used during early debugging.  
  - `check_levels.py` – Print sample rate and level statistics for WAV files.  
  - `metrics_quick.py` – Simple spectral-change metrics for evaluation.

- `templates/` – Saved spectral banks.  
  - `violin_bank.npz` – Learned violin spectral bank.  
  - `piano_bank.npz` – Learned piano spectral bank.  
  - `perc_bank.npz` – Learned percussion spectral bank.

- `requirements.txt` – Python dependencies.  
- `.gitignore` – Ignore rules for audio datasets, venvs and build artefacts.  
- `README.md` – This document.  

---

## 3. Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/JunweiQu/elec5305-project-540947661.git
   cd elec5305-project-540947661
   ```

2. **Create and activate a virtual environment (recommended)**

   ```bash
   python -m venv .venv
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # or Command Prompt:
   .venv\Scripts\activate.bat
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

The code was developed with Python 3.10. The GUI uses only standard Tkinter, which is bundled with normal CPython installations.

---

## 4. Preparing the Instrument Banks

### 4.1 Download Iowa MIS single-note datasets

This project uses the **University of Iowa Musical Instrument Samples (MIS)** database.  
I downloaded:

- Violin single notes,  
- Piano single notes (mf dynamic),  
- A small set of hand-percussion samples.

Place the raw AIF files in:

- `assets/iowa_raw/` for violin,  
- `assets/piano_raw/` for piano,  
- `assets/perc_raw/` for percussion.

If your paths differ, you can edit the constants defined at the top of the `prepare_iowa_*.py` scripts.

### 4.2 Convert AIF to cleaned WAV

Run:

```bash
python src/prepare_iowa_violin.py
python src/prepare_iowa_piano.py
python src/prepare_iowa_perc.py
```

Each script:

- Reads all AIF files from the corresponding `*_raw` folder,  
- Converts them to mono WAV at a consistent sample rate,  
- Trims leading and trailing silence,  
- Normalises the peak level, and  
- Saves the cleaned files to `assets/iowa_wav/`, `assets/piano_wav/` and `assets/perc_wav/`.

### 4.3 Build spectral banks

Then run:

```bash
python src/build_violin_bank.py
python src/build_piano_bank.py
python src/build_perc_bank.py
```

Each script:

- Performs WORLD analysis on every cleaned single note,  
- Aligns spectral envelopes on a fixed frequency grid,  
- Aggregates them on a semitone grid, and  
- Saves the averaged templates into `.npz` files in `templates/`.

These `.npz` files are later loaded by `baseline_world.py` and the apps.

---

## 5. Running Timbre Transfer

### 5.1 Prepare an input WAV

Place your input file under `assets/`, for example:

- `assets/piano_canon.wav`

Optionally, run:

```bash
python src/prepare_input.py assets/piano_canon.wav
```

This script ensures that the file is mono, uses a supported sampling rate and has a safe peak level.

### 5.2 Command-line app (`timbre_app_cli.py`)

Start the CLI:

```bash
python src/timbre_app_cli.py
```

The script will ask you to:

1. Enter the input WAV path (e.g. `assets/piano_canon.wav`), and  
2. Choose a target timbre:

   - `1` – Violin  
   - `2` – Piano  
   - `3` – Drum / percussion  

The program then:

- Runs WORLD analysis on the input (F0, spectral envelope, aperiodicity),  
- Synthesises a **baseline reconstruction** with the original envelope (`recon_world.wav`),  
- Replaces the spectral envelope using the chosen template bank with a blending factor, and  
- Synthesises the converted signal and writes it to `reports/audio/`:

  - `recon_world.wav`  
  - `demo_violin.wav`  
  - `demo_piano.wav`  
  - `demo_drum.wav`  

Only the relevant demo file is updated for each run.

### 5.3 GUI app (`timbre_app_gui.py`)

To demonstrate the project to non-technical users, a small Tkinter GUI is also provided:

```bash
python src/timbre_app_gui.py
```

The GUI allows you to:

1. Browse and select an input WAV file,  
2. Choose one of the three target timbres via radio buttons, and  
3. Click “Run conversion” and wait for the log to report completion.

Internally, the GUI calls the same functions as the CLI and writes output WAV files into `reports/audio/`.  
On my local Windows machine I additionally built a standalone `.exe` using PyInstaller (not committed to git due to file size).

---

## 6. Quick Sanity Checks and Metrics

### 6.1 Level checks

```bash
python src/check_levels.py
```

This prints, for each key WAV file (input, reconstruction and demos):

- Sample rate,  
- Minimum and maximum sample values,  
- Mean absolute value.

This helps detect silent or clipped outputs.

### 6.2 Simple spectral-change metrics

```bash
python src/metrics_quick.py
```

This script loads the baseline reconstruction and one of the converted signals, then computes:

- Average log-spectral distance between them, and  
- Basic RMS statistics.

These numbers were used in the report to compare how strongly each target timbre modifies the spectral envelope.

---

## 7. Summary of Experimental Findings

I carried out three main sets of experiments:

1. **Piano → Violin**  
   - Input: monophonic piano excerpt (Canon in D).  
   - Output: recognisably string-like timbre with preserved pitch and rhythm, but with softened attacks and limited expressiveness (no natural vibrato).

2. **Piano → Piano (self-transfer)**  
   - Used as a sanity check to confirm that the bank construction and blending behave sensibly.  
   - Output remains close to the original, with small but measurable spectral differences.

3. **Piano → Drum / Percussion**  
   - Stress test with a very different target.  
   - Output becomes a rhythmic, percussive texture rather than a realistic drum performance, revealing the limits of using only harmonic spectral envelopes.

Key observations:

- WORLD reconstruction is generally very close to the input for clean, monophonic signals.  
- Timbre transfer works best on **simple melodic lines** with a clear F0 trajectory.  
- Mixed or highly polyphonic audio causes artefacts because the whole mixture is transformed together.  
- Percussion is particularly challenging for this framework because transient and noise components are not explicitly modelled.

---

## 8. Limitations and Future Work

This project intentionally uses a **classical signal-processing pipeline** instead of deep learning. As a result, there are clear limitations:

- No explicit separation between melody and accompaniment,  
- Dynamics and articulation are not modelled; everything is frame-wise and stationary, and  
- Percussion modelling is weak because the approach focuses on harmonic envelopes.

Possible extensions include:

- Applying **harmonic–percussive source separation** before timbre transfer,  
- Using pitch-adaptive or energy-adaptive blending factors instead of a fixed value,  
- Extending the banks to more instruments (e.g. flute, clarinet, erhu) and more dynamic levels, and  
- Comparing this classical pipeline against a small neural vocoder or diffusion-based approach.

---

## 9. Acknowledgements

- **WORLD vocoder** – M. Morise et al., “WORLD: A Vocoder-Based High-Quality Speech Synthesis System”, IEICE Transactions on Information and Systems, 2016.  
- **Musical Instrument Samples (MIS)** – University of Iowa Electronic Music Studios, for making the single-note datasets publicly available.  
- **ELEC5305 teaching staff**, especially Craig Jin, for feedback on the proposal, research question and report structure.

## Offline GUI executable

For quick demonstration, we provide a pre-built Windows executable.

- **Download**:  
  Download `OfflineTimbreTransfer_Windows.exe` from the [`bin` folder](./bin/OfflineTimbreTransfer_Windows.exe) in this repository.

- **System requirements**:
  - Windows 10/11, 64-bit
  - No Python installation is required.

- **How to use**:
  1. Double-click `OfflineTimbreTransfer_Windows.exe`.
  2. Click **Browse...** and select a mono WAV file (e.g. `assets/piano_canon.wav`).
  3. Choose a target timbre:
     - Violin
     - Piano
     - Drum / Percussion
  4. Click **Run conversion**.
  5. The converted WAV files will be written to the `reports/audio` folder
     inside the same directory as the executable.

> On first run, Windows SmartScreen may show a warning because this is not a
> signed application. Click “More info” → “Run anyway” to continue.
