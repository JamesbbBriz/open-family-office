#!/usr/bin/env python3
"""Rebuild the public synthetic dashboard from the canonical package implementation."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from open_family_office.dashboard import build_public_demo

if __name__ == "__main__":
    target = build_public_demo()
    print("Built offline Tailwind + Plotly dashboard:", target.stat().st_size, "bytes")
