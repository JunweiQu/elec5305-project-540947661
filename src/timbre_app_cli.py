# -*- coding: utf-8 -*-
"""
timbre_app_cli.py — simple command-line front-end for the timbre transfer system.

This script lets the user:
  1. Type an input audio path.
  2. Choose a target timbre (violin / piano / drum).
  3. Run WORLD-based timbre transfer using baseline_world.run_world().
"""

from pathlib import Path

from baseline_world import run_world


def main() -> None:
    print("=== Offline Timbre Transfer Tool (WORLD + single-note banks) ===")
    inp = input("Enter input audio path (e.g. assets\\piano_canon.wav): ").strip()
    if not inp:
        inp = "assets\\input_demo.wav"
        print(f"No path given. Using default: {inp}")

    print("\nAvailable target timbres:")
    print("  1 = Violin")
    print("  2 = Piano")
    print("  3 = Drum / Percussion")
    choice = input("Choose target timbre (1 / 2 / 3): ").strip() or "1"

    if choice == "1":
        target = "violin"
    elif choice == "2":
        target = "piano"
    elif choice == "3":
        target = "drum"
    else:
        print("Unknown choice. Defaulting to violin.")
        target = "violin"

    run_world(Path(inp), target)


if __name__ == "__main__":
    main()
