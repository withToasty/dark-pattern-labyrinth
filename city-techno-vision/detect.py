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

from src.camera_metadata import read_camera_metadata
from src.detector import (
    DEFAULT_CITY_CLASSES,
    DEFAULT_CONFIDENCE_THRESHOLD,
    DEFAULT_WORLD_MODEL_ID,
    ObjectDetector,
    merge_detections,
)
from src.export import build_result, write_json, write_yaml
from src.fence_detector import (
    DEFAULT_FENCE_MODEL_ID,
    DEFAULT_SEGMENTATION_CLASSES,
    DEFAULT_SEGMENTATION_THRESHOLD,
    CityscapesDetector,
    mask_to_detections,
)
from src.horizon import DistortionSpec, estimate_horizon, generic_ultrawide_distortion
from src.visualize import draw_detections, draw_horizon


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--image", required=True, help="path to the input image")
    parser.add_argument("--output-dir", default="output", help="directory for outputs (default: output/)")
    parser.add_argument(
        "--model",
        default="yolov8n-oiv7.pt",
        help="primary Ultralytics YOLO model (default: yolov8n-oiv7.pt, Open Images V7 / 601 classes)",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=DEFAULT_CONFIDENCE_THRESHOLD,
        help=f"primary YOLO confidence threshold (default: {DEFAULT_CONFIDENCE_THRESHOLD})",
    )
    parser.add_argument(
        "--world-model",
        default=DEFAULT_WORLD_MODEL_ID,
        help=(
            "supplemental open-vocabulary YOLO-World model; pass an empty string to disable "
            f"(default: {DEFAULT_WORLD_MODEL_ID})"
        ),
    )
    parser.add_argument(
        "--world-conf",
        type=float,
        default=DEFAULT_CONFIDENCE_THRESHOLD,
        help=f"YOLO-World confidence threshold (default: {DEFAULT_CONFIDENCE_THRESHOLD})",
    )
    parser.add_argument(
        "--classes",
        default=None,
        help=(
            "comma-separated YOLO-World vocabulary. If omitted, a broad built-in city-scene "
            "vocabulary is used."
        ),
    )
    parser.add_argument(
        "--fence-model",
        default=DEFAULT_FENCE_MODEL_ID,
        help=(
            "Hugging Face SegFormer/Cityscapes model. The historical flag name is kept for "
            "compatibility, but the model now extracts multiple static scene classes."
        ),
    )
    parser.add_argument(
        "--seg-conf",
        type=float,
        default=DEFAULT_SEGMENTATION_THRESHOLD,
        help=f"semantic-segmentation probability threshold (default: {DEFAULT_SEGMENTATION_THRESHOLD})",
    )
    parser.add_argument(
        "--seg-classes",
        default=None,
        help=(
            "comma-separated Cityscapes classes for segmentation. Default: "
            + ",".join(DEFAULT_SEGMENTATION_CLASSES)
        ),
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


def _parse_csv(value: str | None, default) -> list[str]:
    if value is None:
        return list(default)
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> None:
    args = parse_args()
    image_path = Path(args.image)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    image = cv2.imread(str(image_path))
    if image is None:
        raise SystemExit(f"could not read image: {image_path}")
    height, width = image.shape[:2]

    world_classes = _parse_csv(args.classes, DEFAULT_CITY_CLASSES)
    seg_classes = _parse_csv(args.seg_classes, DEFAULT_SEGMENTATION_CLASSES)

    # Pass 1: broad fixed taxonomy (Open Images V7 by default).
    primary_is_world = "world" in args.model.lower()
    primary_detector = ObjectDetector(
        model_path=args.model,
        confidence_threshold=args.conf,
        classes=world_classes if primary_is_world else None,
        source="yolo_world_primary" if primary_is_world else "yolo_oiv7",
    )
    detections = primary_detector.detect(str(image_path))
    print(f"primary detections  -> {len(detections)} (conf >= {args.conf:g})")

    # Pass 2: open vocabulary. It is supplemental, so failure does not discard the
    # useful fixed-taxonomy detections from pass 1.
    world_detections = []
    if args.world_model and args.world_model != args.model:
        try:
            world_detector = ObjectDetector(
                model_path=args.world_model,
                confidence_threshold=args.world_conf,
                classes=world_classes,
                source="yolo_world",
            )
            world_detections = world_detector.detect(str(image_path))
        except (OSError, RuntimeError, ValueError) as exc:
            print(f"warning: YOLO-World unavailable; continuing without it: {exc}")
        else:
            detections = merge_detections(detections, world_detections)
            print(
                f"world detections    -> {len(world_detections)} "
                f"(conf >= {args.world_conf:g}, classes={len(world_classes)})"
            )

    # Pass 3: semantic scene regions. This turns broad surfaces such as road,
    # sidewalk, building and sky into the same bbox-based Detection format.
    if args.fence_model:
        try:
            scene_detector = CityscapesDetector(
                model_path=args.fence_model,
                confidence_threshold=args.seg_conf,
                class_names=seg_classes,
            )
            scene_masks = scene_detector.predict_masks(image)
        except (RuntimeError, ValueError) as exc:
            print(f"warning: scene segmentation unavailable; continuing with YOLO results: {exc}")
        else:
            scene_lists = []
            for label, mask in scene_masks.items():
                class_detections = mask_to_detections(
                    mask,
                    threshold=scene_detector.confidence_threshold,
                    min_area=scene_detector.min_area,
                    label=label,
                )
                scene_lists.append(class_detections)
                if class_detections:
                    print(f"seg {label:<10} -> {len(class_detections)}")
            scene_detections = merge_detections(*scene_lists)
            detections = merge_detections(detections, scene_detections)

            # Keep the existing fence-mask artifact for compatibility/debugging.
            if "fence" in scene_masks:
                mask_path = output_dir / "fence_mask.png"
                cv2.imwrite(str(mask_path), (scene_masks["fence"] * 255).astype("uint8"))
                print(f"fence mask         -> {mask_path}")

    camera = read_camera_metadata(image_path)
    effective_lens_mode = camera.lens_mode if args.lens_mode == "auto" else args.lens_mode
    distortion = None
    if args.curve_strength is not None:
        distortion = DistortionSpec(
            source="manual_curve_strength",
            curve_strength=args.curve_strength,
            is_approximation=True,
            basis="--curve-strength",
        )
    elif effective_lens_mode == "ultrawide":
        if args.lens_mode == "auto":
            if camera.focal_length_35mm is not None:
                basis = f"EXIF focal_length_35mm={camera.focal_length_35mm:g}"
            elif camera.lens_model:
                basis = f"EXIF lens_model={camera.lens_model}"
            else:
                basis = "EXIF ultrawide hint"
            distortion = generic_ultrawide_distortion("exif_heuristic", basis=basis)
        else:
            distortion = generic_ultrawide_distortion(
                "manual_lens_mode",
                basis="--lens-mode ultrawide",
            )

    horizon = None if args.no_horizon else estimate_horizon(image, distortion=distortion)

    annotated = draw_detections(image, detections)
    if horizon is not None:
        annotated = draw_horizon(annotated, horizon)
    annotated_path = output_dir / f"{image_path.stem}_detected{image_path.suffix}"
    cv2.imwrite(str(annotated_path), annotated)

    result = build_result(image_path.name, width, height, detections)
    camera_data = camera.to_dict()
    camera_data["lens_mode_effective"] = effective_lens_mode
    camera_data["lens_mode_source"] = "exif" if args.lens_mode == "auto" else "manual"
    result["image"]["camera"] = camera_data
    result["detector_settings"] = {
        "primary_model": args.model,
        "primary_conf": args.conf,
        "world_model": args.world_model or None,
        "world_conf": args.world_conf if args.world_model else None,
        "world_classes": world_classes if args.world_model else [],
        "segmentation_model": args.fence_model or None,
        "segmentation_conf": args.seg_conf if args.fence_model else None,
        "segmentation_classes": seg_classes if args.fence_model else [],
    }
    if horizon is not None:
        result["scene_geometry"] = {"horizon": horizon.to_dict()}

    json_path = output_dir / "detections.json"
    yaml_path = output_dir / "detections.yaml"
    write_json(result, json_path)
    write_yaml(result, yaml_path)

    print(f"detected {len(detections)} object/region(s)")
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
