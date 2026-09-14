#!/usr/bin/env python3
"""Validate the public CarPaint-PMD multi-representation dataset."""

from __future__ import annotations

import struct
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPRESENTATIONS = ("AP", "sin0", "sin1", "sin2", "sin3")
EXPECTED_SAMPLES = {"train": 2002, "val": 500}
EXPECTED_BOXES = {
    "train": Counter({0: 1646, 1: 1209, 2: 1425, 3: 199, 4: 113, 5: 321, 6: 120}),
    "val": Counter({0: 526, 1: 289, 2: 405, 3: 51, 4: 17, 5: 79, 6: 37}),
}


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"Invalid PNG header: {path}")
    return struct.unpack(">II", header[16:24])


def parse_label(path: Path) -> Counter[int]:
    counts: Counter[int] = Counter()
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        fields = line.split()
        if len(fields) != 5:
            raise ValueError(f"Expected five YOLO fields at {path}:{line_number}")
        class_id = int(fields[0])
        if class_id not in range(7):
            raise ValueError(f"Invalid class ID at {path}:{line_number}: {class_id}")
        coordinates = [float(value) for value in fields[1:]]
        if any(value < 0.0 or value > 1.0 for value in coordinates):
            raise ValueError(f"Coordinate outside [0, 1] at {path}:{line_number}")
        counts[class_id] += 1
    return counts


def main() -> None:
    splits: dict[str, list[str]] = {}
    for split, expected_count in EXPECTED_SAMPLES.items():
        split_path = ROOT / f"{split}.txt"
        sample_ids = [line.strip() for line in split_path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
        if len(sample_ids) != expected_count or len(set(sample_ids)) != expected_count:
            raise ValueError(f"Unexpected or duplicate entries in {split_path}")
        if any(Path(sample_id).name != sample_id or Path(sample_id).suffix for sample_id in sample_ids):
            raise ValueError(f"Split entries must be extension-free basenames: {split_path}")
        splits[split] = sample_ids

    if set(splits["train"]) & set(splits["val"]):
        raise ValueError("Train and validation splits overlap")
    all_ids = set(splits["train"]) | set(splits["val"])

    label_dir = ROOT / "labels"
    label_paths = sorted(label_dir.glob("*.txt"))
    if len(label_paths) != len(all_ids) or {path.stem for path in label_paths} != all_ids:
        raise ValueError("The shared label set does not match the split files")

    for representation in REPRESENTATIONS:
        image_dir = ROOT / "images" / representation
        image_paths = sorted(image_dir.glob("*.png"))
        if len(image_paths) != len(all_ids) or {path.stem for path in image_paths} != all_ids:
            raise ValueError(f"Unexpected image set in {image_dir}")
        for image_path in image_paths:
            if png_size(image_path) != (300, 300):
                raise ValueError(f"Unexpected image dimensions: {image_path}")

    for split, sample_ids in splits.items():
        class_counts: Counter[int] = Counter()
        for sample_id in sample_ids:
            class_counts.update(parse_label(label_dir / f"{sample_id}.txt"))
        if class_counts != EXPECTED_BOXES[split]:
            raise ValueError(
                f"Unexpected class counts in {split}: observed={dict(class_counts)}, "
                f"expected={dict(EXPECTED_BOXES[split])}"
            )

    print("Dataset validation passed.")
    print("Samples: 2,502 (train 2,002; validation 500)")
    print("Bounding boxes: 6,437 (train 5,033; validation 1,404)")
    print("Representations: AP, sin0, sin1, sin2, sin3")
    print("Image size: 300 x 300 pixels")


if __name__ == "__main__":
    main()
