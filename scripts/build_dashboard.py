#!/usr/bin/env python3
"""Compatibility wrapper around the canonical package dashboard implementation."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from open_family_office.dashboard import payload, render, export_dashboard, build_public_demo

def main():
    target = build_public_demo()
    print("Built offline Tailwind + Plotly dashboard:", target.stat().st_size, "bytes")
    return target

if __name__ == "__main__":
    main()
