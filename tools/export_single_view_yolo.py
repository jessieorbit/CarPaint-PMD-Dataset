#!/usr/bin/env python3
"""Export one representation as a conventional single-view YOLO dataset."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ("AP", "sin0", "sin1", "sin2", "sin3")
CLASS_NAMES = ("breakage", "inclusion", "scratch", "crater", "run", "bulge", "condensate")


def transfer(source: Path, destination: Path, mode: str) -> None:
    if mode == "copy":
        shutil.copy2(source, destination)
    else:
        os.link(source, destination)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--view", required=True, choices=VIEWS, help="Imaging representation to export")
    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory (default: <dataset>/exports/yolo_<view>)",
    )
    parser.add_argument(
        "--mode",
        choices=("copy", "hardlink"),
        default="copy",
        help="Copy files or create same-filesystem hard links (default: copy)",
    )
    args = parser.parse_args()

    output = (args.output or (ROOT / "exports" / f"yolo_{args.view}")).resolve()
    if output.exists():
        raise FileExistsError(f"Output already exists; choose a new directory: {output}")

    for split in ("train", "val"):
        image_output = output / "images" / split
        label_output = output / "labels" / split
        image_output.mkdir(parents=True)
        label_output.mkdir(parents=True)

        sample_ids = [
            line.strip()
            for line in (ROOT / f"{split}.txt").read_text(encoding="utf-8-sig").splitlines()
            if line.strip()
        ]
        for sample_id in sample_ids:
            transfer(ROOT / "images" / args.view / f"{sample_id}.png", image_output / f"{sample_id}.png", args.mode)
            transfer(ROOT / "labels" / f"{sample_id}.txt", label_output / f"{sample_id}.txt", args.mode)

    yaml_lines = ["train: images/train", "val: images/val", "", "names:"]
    yaml_lines.extend(f"  {index}: {name}" for index, name in enumerate(CLASS_NAMES))
    (output / "data.yaml").write_text("\n".join(yaml_lines) + "\n", encoding="utf-8")
    print(f"Exported {args.view} dataset to: {output}")


if __name__ == "__main__":
    main()
