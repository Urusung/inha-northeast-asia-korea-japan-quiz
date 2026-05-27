#!/usr/bin/env python3
"""Extract readable slide text from lecture PPTX files into JSON."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


TEXT_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}t"


def natural_key(path: Path) -> list[object]:
    value = unicodedata.normalize("NFC", path.name)
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", value)]


def slide_number(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 0


def clean_text(value: str) -> str:
    value = unicodedata.normalize("NFC", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def extract_slide_text(xml_bytes: bytes) -> list[str]:
    root = ET.fromstring(xml_bytes)
    lines: list[str] = []
    current: list[str] = []

    for elem in root.iter():
        if elem.tag == TEXT_NS and elem.text:
            text = clean_text(elem.text)
            if text:
                current.append(text)
        elif elem.tag.endswith("}p") and current:
            line = clean_text(" ".join(current))
            if line and line not in lines:
                lines.append(line)
            current = []

    if current:
        line = clean_text(" ".join(current))
        if line and line not in lines:
            lines.append(line)

    return lines


def extract_pptx(path: Path) -> dict[str, object]:
    slides: list[dict[str, object]] = []
    with zipfile.ZipFile(path) as archive:
        names = sorted(
            [name for name in archive.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", name)],
            key=slide_number,
        )
        for index, name in enumerate(names, start=1):
            lines = extract_slide_text(archive.read(name))
            if lines:
                slides.append({"number": index, "lines": lines})

    return {
        "file": unicodedata.normalize("NFC", path.name),
        "path": str(path),
        "slide_count": len(names),
        "slides_with_text": len(slides),
        "slides": slides,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--week", type=str, help="Only include filenames containing this week number pattern, e.g. 6-")
    args = parser.parse_args()

    files = [path for path in args.input_dir.glob("*.pptx") if not path.name.startswith("~$")]
    if args.week:
        files = [path for path in files if args.week in unicodedata.normalize("NFC", path.name)]

    payload = [extract_pptx(path) for path in sorted(files, key=natural_key)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"extracted {len(payload)} pptx files to {args.output}")


if __name__ == "__main__":
    main()
