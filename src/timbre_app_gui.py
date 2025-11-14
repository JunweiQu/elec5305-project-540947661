# -*- coding: utf-8 -*-
"""
timbre_app_gui.py — offline timbre transfer tool with a simple Tkinter GUI.

The GUI allows the user to:
  - browse and select an input WAV file
  - choose a target timbre (violin / piano / drum)
  - run WORLD-based timbre transfer
  - see log messages in the window
"""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from baseline_world import run_world


ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"
OUT_DIR = ROOT / "reports" / "audio"


def browse_file() -> None:
    """Open a file dialog and put the chosen path into the entry widget."""
    path = filedialog.askopenfilename(
        title="Select input audio file",
        initialdir=str(ASSETS_DIR),
        filetypes=[
            ("WAV audio", "*.wav"),
            ("All files", "*.*"),
        ],
    )
    if path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, path)


def run_conversion() -> None:
    """Run timbre transfer using baseline_world.run_world()."""
    path_str = entry_path.get().strip()
    if not path_str:
        messagebox.showwarning("Warning", "Please select an input audio file first.")
        return

    p = Path(path_str)
    if not p.is_file():
        messagebox.showerror("Error", f"File not found:\n{p}")
        return

    # Map the radio-button label to an internal target string
    target_label = timbre_var.get()
    target_map = {
        "Violin": "violin",
        "Piano": "piano",
        "Drum / Percussion": "drum",
    }
    target = target_map.get(target_label, "violin")

    try:
        log(f"Starting conversion: {p.name} -> {target}\n")
        root.update_idletasks()

        run_world(p, target)

        OUT_DIR.mkdir(parents=True, exist_ok=True)
        log(f"Done. Output files are stored in: {OUT_DIR}\n")
        messagebox.showinfo("Finished", f"Conversion finished.\nOutputs are in:\n{OUT_DIR}")
    except Exception as e:
        log(f"Error: {e}\n")
        messagebox.showerror("Error", f"Conversion failed:\n{e}")


def log(text: str) -> None:
    """Append text to the log window."""
    text_log.insert(tk.END, text)
    text_log.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Offline Timbre Transfer (WORLD + Iowa)")
    root.geometry("720x420")

    # Row 1: file selection
    frame_file = tk.Frame(root)
    frame_file.pack(fill="x", padx=10, pady=10)

    tk.Label(frame_file, text="Input audio file:").pack(side="left")
    entry_path = tk.Entry(frame_file, width=60)
    entry_path.pack(side="left", padx=5)
    tk.Button(frame_file, text="Browse...", command=browse_file).pack(side="left")

    # Row 2: target timbre
    frame_timbre = tk.LabelFrame(root, text="Target timbre")
    frame_timbre.pack(fill="x", padx=10, pady=5)

    timbre_var = tk.StringVar(value="Violin")
    for label in ["Violin", "Piano", "Drum / Percussion"]:
        tk.Radiobutton(
            frame_timbre,
            text=label,
            variable=timbre_var,
            value=label,
        ).pack(anchor="w")

    # Row 3: run button and hint
    frame_btn = tk.Frame(root)
    frame_btn.pack(fill="x", padx=10, pady=5)

    tk.Button(frame_btn, text="Run conversion", command=run_conversion).pack(side="left")
    tk.Label(
        frame_btn,
        text="Output WAV files are written to the 'reports/audio' folder.",
        fg="gray",
    ).pack(side="left", padx=10)

    # Row 4: log window
    frame_log = tk.LabelFrame(root, text="Log")
    frame_log.pack(fill="both", expand=True, padx=10, pady=5)

    text_log = tk.Text(frame_log, height=12)
    text_log.pack(fill="both", expand=True)

    log("Ready. Select an input WAV file, choose a target timbre, and click 'Run conversion'.\n")

    root.mainloop()
