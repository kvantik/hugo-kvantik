#!/usr/bin/env python3
"""Generate archive covers using Poppler and ImageMagick; report missing sources."""

from pathlib import Path
import argparse
import json
import math
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
PDFS = ROOT / "static-old/articles/files/pdf"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--web-source-dir", type=Path,
                        help="Directory containing downloaded files listed in retina-related-web.json")
    parser.add_argument("--poster-source-dir", type=Path,
                        help="Directory containing poster-1.pdf, poster-2.pdf, poster-3-hq.pdf")
    parser.add_argument("--only", nargs="+", help="Generate only these image stems")
    parser.add_argument("--almanac-one-cover", type=Path,
                        help="PDF spread for almanac 1 (453 mm wide, front cover is the rightmost 220 mm)")
    parser.add_argument("--fedin-cover", type=Path,
                        help="New edition cover spread (450 mm wide, front cover is the rightmost 218 mm)")
    args = parser.parse_args()
    web = json.loads((ROOT / "scripts/retina-related-web.json").read_text())
    images = re.findall(r"img: (\S+)", (ROOT / "data/related_titles.yaml").read_text())
    with tempfile.TemporaryDirectory() as tmp:
        for image in images:
            original = ROOT / "static" / image
            name = original.stem
            if args.only and name not in args.only:
                continue
            rotation = 0
            front_cover = name == "almanac-1" and args.almanac_one_cover is not None
            fedin_cover = name == "biblio-pereputanica" and args.fedin_cover is not None
            web_source = (args.web_source_dir / web[name].rsplit("/", 1)[1]
                          if args.web_source_dir and name in web else None)
            if name == "almanac-1" and not front_cover:
                print("Skipped almanac-1: PDF has no front cover")
                continue
            if front_cover:
                source = args.almanac_one_cover
            elif fedin_cover:
                source = args.fedin_cover
            elif web_source:
                source = web_source
            elif name.startswith("posters-") and args.poster_source_dir:
                number = name.split("-")[1]
                filename = "poster-3-hq.pdf" if number == "3" else f"poster-{number}.pdf"
                source = args.poster_source_dir / filename
                rotation = 90 if number in ("2", "3") else 0
            elif name.startswith("almanac-"):
                source = PDFS / (name.replace("-", "") + ".pdf")
            elif name.startswith("calendar_"):
                source = PDFS / ("Календарь " + name.split("_")[1] + ".pdf")
            elif name == "biblio-pereputanica":
                print("Skipped biblio-pereputanica: supply --fedin-cover for the new edition")
                continue
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
                render_width = math.ceil(width * 453 / 220) if front_cover else (height if rotation else width)
                if fedin_cover:
                    render_width = math.ceil(width * 450 / 218)
                subprocess.run([
                    "pdftoppm", "-f", "1", "-singlefile", "-scale-to-x", str(render_width),
                    "-scale-to-y", "-1", "-png", str(source), str(prefix),
                ], check=True)
                rendered = prefix.with_suffix(".png")
            output = original.with_name(name + "@2x.jpg")
            # Fit without distortion; retain the original image's layout dimensions.
            crop = ["-gravity", "east", "-crop", f"{width}x0+0+0", "+repage"] if front_cover or fedin_cover else []
            subprocess.run([
                "magick", str(rendered), *crop, "-rotate", str(rotation), "-resize", f"{width}x{height}",
                "-background", "white", "-gravity", "center", "-extent", f"{width}x{height}",
                "-quality", "90", str(output),
            ], check=True)
            if fedin_cover:
                subprocess.run([
                    "magick", str(output), "-resize", f"{width // 2}x{height // 2}",
                    "-quality", "90", str(original),
                ], check=True)
            print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
