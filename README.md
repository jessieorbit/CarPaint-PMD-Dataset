# CarPaint-PMD-Dataset

[English](README.md) | [简体中文](README_zh-CN.md)

This dataset contains 2,502 spatially aligned multi-representation samples for car paint defect detection. Each sample consists of one absolute phase map (`AP`) and four corresponding phase-shifted sinusoidal fringe images (`sin0`--`sin3`) obtained in a Phase Measuring Deflectometry imaging process. All five images belonging to a sample share the same basename.

## Dataset organization

```text
CarPaint-PMD-Dataset/
|-- images/
|   |-- AP/
|   |-- sin0/
|   |-- sin1/
|   |-- sin2/
|   `-- sin3/
|-- labels/
|-- train.txt
|-- val.txt
|-- dataset.yaml
|-- examples/
`-- tools/
    |-- export_single_view_yolo.py
    `-- verify_dataset.py
```

Each representation directory contains the complete set of 2,502 images. `labels` contains one shared set of 2,502 YOLO-format annotation files. `train.txt` and `val.txt` contain the sample basenames used for the experimental split, without filename extensions or representation-specific paths.

## Dataset statistics

| Split | Samples | Bounding boxes |
|---|---:|---:|
| Train | 2,002 | 5,033 |
| Validation | 500 | 1,404 |
| Total | 2,502 | 6,437 |

Empty label files denote negative samples without annotated defects.

## Classes

YOLO class identifiers are zero-based:

| ID | Class | Train instances | Validation instances | Total |
|---:|---|---:|---:|---:|
| 0 | breakage | 1,646 | 526 | 2,172 |
| 1 | inclusion | 1,209 | 289 | 1,498 |
| 2 | scratch | 1,425 | 405 | 1,830 |
| 3 | crater | 199 | 51 | 250 |
| 4 | run | 113 | 17 | 130 |
| 5 | bulge | 321 | 79 | 400 |
| 6 | condensate | 120 | 37 | 157 |

Each annotation row follows the standard YOLO detection format:

```text
class_id x_center y_center width height
```

All four coordinates are normalized to `[0, 1]`.

## Multi-representation use

For a sample identifier read from `train.txt` or `val.txt`, load the aligned inputs and annotation as follows:

```text
images/AP/{sample_id}.png
images/sin0/{sample_id}.png
images/sin1/{sample_id}.png
images/sin2/{sample_id}.png
images/sin3/{sample_id}.png
labels/{sample_id}.txt
```

`dataset.yaml` describes this multi-representation layout. It is intended for a custom multi-input data loader; stock Ultralytics YOLO accepts split text files but does not natively consume five aligned input images per sample.

## Exporting a standard single-view YOLO dataset

To reproduce a conventional single-representation baseline, export any representation to a standard Ultralytics-compatible directory:

```bash
python tools/export_single_view_yolo.py --view AP
python tools/export_single_view_yolo.py --view sin0
```

The export contains `images/{train,val}`, `labels/{train,val}`, and a local `data.yaml`. Use `--mode hardlink` to avoid duplicating image bytes when the source and output are on the same filesystem.

## Validation

Run the release validator after downloading or modifying the dataset:

```bash
python tools/verify_dataset.py
```

The validator checks split integrity, cross-representation filename alignment, PNG dimensions, image-label correspondence, YOLO coordinates, and class counts.

## Examples

The following curated samples illustrate all seven defect classes and their
appearance across the absolute phase map and four phase-shifted fringe images.
`AP (annotated)` shows every ground-truth box in the corresponding
[`label.txt`](#classes) file; the other five images are unmodified dataset
images.

### Breakage

Sample ID: `00_0000_000011_1260_1050_300_300` ([label](examples/breakage/label.txt))

| AP (annotated) | AP | sin0 | sin1 | sin2 | sin3 |
|---|---|---|---|---|---|
| ![Breakage annotated AP](examples/breakage/AP_annotated.png) | ![Breakage AP](examples/breakage/AP.png) | ![Breakage sin0](examples/breakage/sin0.png) | ![Breakage sin1](examples/breakage/sin1.png) | ![Breakage sin2](examples/breakage/sin2.png) | ![Breakage sin3](examples/breakage/sin3.png) |

### Inclusion

Sample ID: `00_0001_000083_1470_1890_300_300` ([label](examples/inclusion/label.txt))

| AP (annotated) | AP | sin0 | sin1 | sin2 | sin3 |
|---|---|---|---|---|---|
| ![Inclusion annotated AP](examples/inclusion/AP_annotated.png) | ![Inclusion AP](examples/inclusion/AP.png) | ![Inclusion sin0](examples/inclusion/sin0.png) | ![Inclusion sin1](examples/inclusion/sin1.png) | ![Inclusion sin2](examples/inclusion/sin2.png) | ![Inclusion sin3](examples/inclusion/sin3.png) |

### Scratch

Sample ID: `00_0015_000547_1470_1680_300_300` ([label](examples/scratch/label.txt))

| AP (annotated) | AP | sin0 | sin1 | sin2 | sin3 |
|---|---|---|---|---|---|
| ![Scratch annotated AP](examples/scratch/AP_annotated.png) | ![Scratch AP](examples/scratch/AP.png) | ![Scratch sin0](examples/scratch/sin0.png) | ![Scratch sin1](examples/scratch/sin1.png) | ![Scratch sin2](examples/scratch/sin2.png) | ![Scratch sin3](examples/scratch/sin3.png) |

### Crater

Sample ID: `00_0005_000291_1260_2132_300_300` ([label](examples/crater/label.txt))

| AP (annotated) | AP | sin0 | sin1 | sin2 | sin3 |
|---|---|---|---|---|---|
| ![Crater annotated AP](examples/crater/AP_annotated.png) | ![Crater AP](examples/crater/AP.png) | ![Crater sin0](examples/crater/sin0.png) | ![Crater sin1](examples/crater/sin1.png) | ![Crater sin2](examples/crater/sin2.png) | ![Crater sin3](examples/crater/sin3.png) |

### Run

Sample ID: `00_0007_000376_1680_0420_300_300` ([label](examples/run/label.txt))

| AP (annotated) | AP | sin0 | sin1 | sin2 | sin3 |
|---|---|---|---|---|---|
| ![Run annotated AP](examples/run/AP_annotated.png) | ![Run AP](examples/run/AP.png) | ![Run sin0](examples/run/sin0.png) | ![Run sin1](examples/run/sin1.png) | ![Run sin2](examples/run/sin2.png) | ![Run sin3](examples/run/sin3.png) |

### Bulge

Sample ID: `00_0023_000819_1470_1260_300_300` ([label](examples/bulge/label.txt))

| AP (annotated) | AP | sin0 | sin1 | sin2 | sin3 |
|---|---|---|---|---|---|
| ![Bulge annotated AP](examples/bulge/AP_annotated.png) | ![Bulge AP](examples/bulge/AP.png) | ![Bulge sin0](examples/bulge/sin0.png) | ![Bulge sin1](examples/bulge/sin1.png) | ![Bulge sin2](examples/bulge/sin2.png) | ![Bulge sin3](examples/bulge/sin3.png) |

### Condensate

Sample ID: `00_0022_000779_1050_1890_300_300` ([label](examples/condensate/label.txt))

| AP (annotated) | AP | sin0 | sin1 | sin2 | sin3 |
|---|---|---|---|---|---|
| ![Condensate annotated AP](examples/condensate/AP_annotated.png) | ![Condensate AP](examples/condensate/AP.png) | ![Condensate sin0](examples/condensate/sin0.png) | ![Condensate sin1](examples/condensate/sin1.png) | ![Condensate sin2](examples/condensate/sin2.png) | ![Condensate sin3](examples/condensate/sin3.png) |

## License

Except where otherwise noted, this repository and the associated dataset are
licensed under the [Creative Commons Attribution-NonCommercial 4.0
International License](https://creativecommons.org/licenses/by-nc/4.0/)
(CC BY-NC 4.0). Reuse must be non-commercial, must provide appropriate
attribution, and must indicate whether changes were made. See [LICENSE](LICENSE)
for details.

## Citation

Citation information will be added when the repository and associated paper metadata are finalized.
