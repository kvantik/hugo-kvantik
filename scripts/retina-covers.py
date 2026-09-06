#!/usr/bin/env python3
"""Render 2x issue covers from PDF first pages (requires Poppler pdftoppm)."""

import argparse
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, nargs="+")
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parents[1] / "static/issue/cover")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for pdf in args.pdf:
        issue = pdf.stem.removesuffix("_sample")
        output = args.output_dir / (issue + "@2x")
        subprocess.run([
            "pdftoppm", "-f", "1", "-singlefile",
            "-scale-to-x", "630", "-scale-to-y", "804",
            "-jpeg", "-jpegopt", "quality=90", str(pdf), str(output),
        ], check=True)
        print(output.with_suffix(".jpg"))


if __name__ == "__main__":
    main()
