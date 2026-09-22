#!/usr/bin/env python3
"""Detect objects and scene geometry in an image and export the results.

    python detect.py --image path/to/photo.jpg --output-dir output/

Produces, in --output-dir:
  <name>_detected<ext>   boxes + reference horizon drawn on the input image
  detections.json        structured detection + scene-geometry results
  detections.yaml        the same results, as YAML

Turning these results into sound is a separate project and does not belong here.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2

from src.export import write_json, write_yaml
from src.fence_detector import DEFAULT_FENCE_MODEL_ID
from src.pipeline import FenceDetectionError, PipelineOptions, run_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--image", required=True, help="path to the input image")
    parser.add_argument("--output-dir", default="output", help="directory for outputs (default: output/)")
    parser.add_argument(
        "--model",
        default="yolov8n-oiv7.pt",
        help="Ultralytics model name or path to weights (default: yolov8n-oiv7.pt, "
        "trained on Open Images V7's 601 classes -- a superset of COCO's 80 that "
        "also covers things like building/skyscraper/tree/window/door/billboard). "
        "Use an open-vocabulary model (e.g. yolov8s-worldv2.pt) to enable --classes.",
    )
    parser.add_argument("--conf", type=float, default=0.15, help="confidence threshold (default: 0.15)")
    parser.add_argument(
        "--fence-model",
        default=DEFAULT_FENCE_MODEL_ID,
        help="Hugging Face model id or local path for the fence-segmentation "
        "model (default: nvidia/segformer-b0-finetuned-cityscapes-"
        "1024-1024, see src/fence_detector.py). Fence detection is required: "
        "if this model can't be loaded or inference fails, the run fails "
        "entirely rather than falling back to a YOLO-only result.",
    )
    parser.add_argument(
        "--classes",
        default=None,
        help="comma-separated list of things to detect, e.g. "
        "'building,sky,cloud,fence,car'. Only works with an open-vocabulary "
        "(YOLO-World) --model; ignored/invalid otherwise. If omitted while "
        "using a world model, falls back to a built-in city-scene vocabulary.",
    )
    parser.add_argument(
        "--lens-mode",
        choices=("auto", "ultrawide", "standard"),
        default="auto",
        help="lens geometry hint for the curved horizon. auto uses EXIF when available; "
        "ultrawide enables a clearly-labelled generic approximation; standard disables it",
    )
    parser.add_argument(
        "--curve-strength",
        type=float,
        default=None,
        help="manual parabolic curve strength as a fraction of image height; "
        "always exported as an approximation, never as measured calibration",
    )
    parser.add_argument(
        "--no-horizon",
        action="store_true",
        help="disable reference horizon estimation",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    image_path = Path(args.image)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    classes = [c.strip() for c in args.classes.split(",") if c.strip()] if args.classes else None
    if classes:
        print(f"classes: {', '.join(classes)}")

    options = PipelineOptions(
        model=args.model,
        confidence=args.conf,
        fence_model=args.fence_model or None,
        classes=classes,
        lens_mode=args.lens_mode,
        curve_strength=args.curve_strength,
        enable_horizon=not args.no_horizon,
    )

    try:
        pipeline_result = run_pipeline(image_path, options)
    except (ValueError, FenceDetectionError) as exc:
        raise SystemExit(str(exc)) from exc

    for warning in pipeline_result.warnings:
        print(f"warning: {warning}")

    # Fence detection is required (run_pipeline raises otherwise), so a
    # successful result always has a mask.
    mask_path = output_dir / "fence_mask.png"
    cv2.imwrite(str(mask_path), (pipeline_result.fence_mask * 255).astype("uint8"))
    fence_count = sum(1 for det in pipeline_result.detections if det.label == "fence")
    print(f"fence detections   -> {fence_count}")
    print(f"fence mask         -> {mask_path}")

    annotated_path = output_dir / f"{image_path.stem}_detected{image_path.suffix}"
    cv2.imwrite(str(annotated_path), pipeline_result.annotated_image)

    json_path = output_dir / "detections.json"
    yaml_path = output_dir / "detections.yaml"
    write_json(pipeline_result.result, json_path)
    write_yaml(pipeline_result.result, yaml_path)

    print(f"detected {len(pipeline_result.detections)} object(s)")
    horizon = pipeline_result.horizon
    if horizon is not None:
        if horizon.detected:
            print(
                "horizon           -> "
                f"center_y={horizon.center_y:.1f}, "
                f"slope={horizon.slope:.4f}, "
                f"confidence={horizon.confidence:.3f}"
            )
            if horizon.distortion is not None:
                print(
                    "horizon curve     -> "
                    f"{horizon.distortion.model}, "
                    f"source={horizon.distortion.source}, "
                    f"approximation={horizon.distortion.is_approximation}"
                )
            else:
                print("horizon curve     -> unavailable (no distortion hint/calibration)")
        else:
            reason = horizon.rejection_reason or "no stable candidate"
            print(f"horizon           -> not detected ({reason})")
    print(f"annotated image -> {annotated_path}")
    print(f"json             -> {json_path}")
    print(f"yaml             -> {yaml_path}")


if __name__ == "__main__":
    main()
