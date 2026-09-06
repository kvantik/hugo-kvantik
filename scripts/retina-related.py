#!/usr/bin/env python3
"""Generate archive covers using Poppler and ImageMagick; report missing sources."""

from pathlib import Path
import argparse
import json
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
PDFS = ROOT / "static-old/articles/files/pdf"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--web-source-dir", type=Path,
                        help="Directory containing downloaded files listed in retina-related-web.json")
    args = parser.parse_args()
    web = json.loads((ROOT / "scripts/retina-related-web.json").read_text())
    images = re.findall(r"img: (\S+)", (ROOT / "data/related_titles.yaml").read_text())
    with tempfile.TemporaryDirectory() as tmp:
        for image in images:
            original = ROOT / "static" / image
            name = original.stem
            web_source = (args.web_source_dir / web[name].rsplit("/", 1)[1]
                          if args.web_source_dir and name in web else None)
            if name == "almanac-1":
                print("Skipped almanac-1: PDF has no front cover")
                continue
            if web_source:
                source = web_source
            elif name.startswith("almanac-"):
                source = PDFS / (name.replace("-", "") + ".pdf")
            elif name.startswith("calendar_"):
                source = PDFS / ("Календарь " + name.split("_")[1] + ".pdf")
            elif name == "biblio-pereputanica":
                source = PDFS / "Сергей Федин. Перепутаница.pdf"
            else:
                print(f"Missing PDF: {name}")
                continue
            if not source.is_file():
                print(f"Missing PDF: {source.name}")
                continue
            dimensions = subprocess.check_output(
                ["magick", "identify", "-format", "%w %h", str(original)], text=True)
            width, height = (2 * int(n) for n in dimensions.split())
            prefix = Path(tmp) / "cover"
            if web_source:
                rendered = source
            else:
                subprocess.run([
                    "pdftoppm", "-f", "1", "-singlefile", "-scale-to-x", str(width),
                    "-scale-to-y", "-1", "-png", str(source), str(prefix),
                ], check=True)
                rendered = prefix.with_suffix(".png")
            output = original.with_name(name + "@2x.jpg")
            # Fit without distortion; retain the original image's layout dimensions.
            subprocess.run([
                "magick", str(rendered), "-resize", f"{width}x{height}",
                "-background", "white", "-gravity", "center", "-extent", f"{width}x{height}",
                "-quality", "90", str(output),
            ], check=True)
            print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
