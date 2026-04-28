#!/usr/bin/env python3
"""
KMBR & KPBR Data Pipeline
==========================
Extracts structured content from:
  • KMBR — Kerala Municipal Building Rules  (website, 23 chapters)
  • KPBR — Kerala Panchayat Building Rules 2019 (PDF)

Outputs one Markdown file per chapter under:
  data/building_rules/kmbr/   — KMBR chapters
  data/building_rules/kpbr/   — KPBR chapters

Usage:
  python pipeline.py            # run both
  python pipeline.py --kmbr     # KMBR only
  python pipeline.py --kpbr     # KPBR only
"""

import argparse
import os
import sys
import time


def banner(text: str) -> None:
    width = 60
    print()
    print("=" * width)
    print(f"  {text}")
    print("=" * width)


def run_kmbr(output_dir: str) -> None:
    from extractors.kmbr_extractor import extract_kmbr

    banner("KMBR — Kerala Municipal Building Rules")
    t0 = time.time()
    extract_kmbr(output_dir)
    elapsed = time.time() - t0
    print(f"\n  Done in {elapsed:.1f}s  |  output → {output_dir}")


def run_kpbr(output_dir: str) -> None:
    from extractors.kpbr_extractor import extract_kpbr

    banner("KPBR — Kerala Panchayat Building Rules 2019")
    t0 = time.time()
    extract_kpbr(output_dir)
    elapsed = time.time() - t0
    print(f"\n  Done in {elapsed:.1f}s  |  output → {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="KMBR / KPBR data pipeline")
    parser.add_argument("--kmbr", action="store_true", help="Run KMBR extractor only")
    parser.add_argument("--kpbr", action="store_true", help="Run KPBR extractor only")
    args = parser.parse_args()

    base     = os.path.dirname(os.path.abspath(__file__))
    out_root = os.path.join(base, "data", "building_rules")

    run_both = not args.kmbr and not args.kpbr

    if args.kmbr or run_both:
        run_kmbr(os.path.join(out_root, "kmbr"))

    if args.kpbr or run_both:
        run_kpbr(os.path.join(out_root, "kpbr"))

    banner("Pipeline complete")
    print(f"  All output files are in: {out_root}")
    print()


if __name__ == "__main__":
    main()
