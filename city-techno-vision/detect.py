#!/usr/bin/env python3
"""Detect objects in an image and export the results.

    python detect.py --image path/to/photo.jpg --output-dir output/

Produces, in --output-dir:
  <name>_detected<ext>   the input image with bounding boxes drawn on it
  detections.json        structured detection results
  detections.yaml        the same results, as YAML

This is the image-recognition step only: image in, boxes + labels +
confidences out. Turning that into sound (object-to-sound mapping,
BPM, pitch, rhythm, MIDI/audio generation) is a separate project and
does not belong here.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2

from src.detector import DEFAULT_CITY_CLASSES, ObjectDetector
from src.export import build_result, write_json, write_yaml
from src.visualize import draw_detections


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--image", required=True, help="path to the input image")
    parser.add_argument("--output-dir", default="output", help="directory for outputs (default: output/)")
    parser.add_argument(
        "--model",
        default="yolov8n.pt",
        help="Ultralytics model name or path to weights. Use an open-vocabulary "
        "model (e.g. yolov8s-worldv2.pt) to enable --classes.",
    )
    parser.add_argument("--conf", type=float, default=0.25, help="confidence threshold (default: 0.25)")
    parser.add_argument(
        "--classes",
        default=None,
        help="comma-separated list of things to detect, e.g. "
        "'building,sky,cloud,fence,car'. Only works with an open-vocabulary "
        "(YOLO-World) --model; ignored/invalid otherwise. If omitted while "
        "using a world model, falls back to a built-in city-scene vocabulary.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    image_path = Path(args.image)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    image = cv2.imread(str(image_path))
    if image is None:
        raise SystemExit(f"could not read image: {image_path}")
    height, width = image.shape[:2]

    is_open_vocab_model = "world" in args.model.lower()
    if args.classes:
        classes = [c.strip() for c in args.classes.split(",") if c.strip()]
    elif is_open_vocab_model:
        classes = DEFAULT_CITY_CLASSES
    else:
        classes = None
    if classes:
        print(f"classes: {', '.join(classes)}")

    detector = ObjectDetector(model_path=args.model, confidence_threshold=args.conf, classes=classes)
    detections = detector.detect(str(image_path))

    annotated = draw_detections(image, detections)
    annotated_path = output_dir / f"{image_path.stem}_detected{image_path.suffix}"
    cv2.imwrite(str(annotated_path), annotated)

    result = build_result(image_path.name, width, height, detections)
    json_path = output_dir / "detections.json"
    yaml_path = output_dir / "detections.yaml"
    write_json(result, json_path)
    write_yaml(result, yaml_path)

    print(f"detected {len(detections)} object(s)")
    print(f"annotated image -> {annotated_path}")
    print(f"json             -> {json_path}")
    print(f"yaml             -> {yaml_path}")


if __name__ == "__main__":
    main()
