"""Shared image -> detections/horizon pipeline, used by both detect.py (CLI)
and the web API (web/app.py).

This module does not introduce any new recognition logic; it only wraps the
existing detector/fence_detector/horizon/export/visualize modules behind one
call so both entry points run the same steps and produce the same JSON/YAML
schema. Model weights (YOLO, SegFormer) are cached per-process so repeated
calls don't reload them.

A normal successful analysis is YOLO detection + SegFormer fence detection +
horizon estimation, together -- not YOLO alone. Fence detection is required:
if the SegFormer model can't be loaded or inference fails, run_pipeline()
raises FenceDetectionError rather than returning a YOLO-only result as a
success. This applies identically to the CLI and the web API; there is no
YOLO-only fallback/debug mode. Horizon estimation itself never raises for a
"soft" case -- a `detected: false` horizon is a normal, successful result.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock

import cv2
import numpy as np

from .camera_metadata import read_camera_metadata
from .detector import DEFAULT_CITY_CLASSES, Detection, ObjectDetector, merge_detections
from .export import build_result
from .fence_detector import DEFAULT_FENCE_MODEL_ID, FenceDetector, mask_to_detections
from .horizon import DistortionSpec, HorizonResult, estimate_horizon, generic_ultrawide_distortion
from .visualize import draw_detections, draw_horizon

DEFAULT_MODEL = "yolov8n-oiv7.pt"
DEFAULT_CONFIDENCE = 0.15


@dataclass
class PipelineOptions:
    model: str = DEFAULT_MODEL
    confidence: float = DEFAULT_CONFIDENCE
    fence_model: str | None = DEFAULT_FENCE_MODEL_ID
    classes: list[str] | None = None
    lens_mode: str = "auto"
    curve_strength: float | None = None
    enable_horizon: bool = True


class FenceDetectionError(RuntimeError):
    """Fence detection (SegFormer) failed to load or run. Raised by
    run_pipeline() for both the CLI and the web API -- there is no
    YOLO-only fallback; a run that can't complete fence detection is not a
    successful analysis."""


@dataclass
class PipelineResult:
    result: dict
    annotated_image: np.ndarray
    detections: list[Detection]
    horizon: HorizonResult | None = None
    fence_mask: np.ndarray | None = None
    warnings: list[str] = field(default_factory=list)


class _ModelCache:
    """Loads YOLO/SegFormer weights at most once per process.

    Repeated `run_pipeline` calls (e.g. one per web upload) reuse whatever
    was already loaded instead of re-reading weights from disk each time.
    """

    def __init__(self) -> None:
        self._lock = Lock()
        self._detectors: dict[tuple, ObjectDetector] = {}
        self._fence_detectors: dict[str, FenceDetector | None] = {}
        self._fence_detector_errors: dict[str, str] = {}

    def get_detector(
        self, model_path: str, confidence: float, classes: tuple[str, ...] | None
    ) -> ObjectDetector:
        key = (model_path, confidence, classes)
        with self._lock:
            detector = self._detectors.get(key)
            if detector is None:
                detector = ObjectDetector(
                    model_path=model_path,
                    confidence_threshold=confidence,
                    classes=list(classes) if classes else None,
                )
                self._detectors[key] = detector
            return detector

    def get_fence_detector(self, model_path: str) -> tuple[FenceDetector | None, str | None]:
        """Returns (detector, error). `error` is set (and detector is None)
        when loading previously failed -- the failure is cached too, so a
        network-blocked model isn't retried on every upload."""
        with self._lock:
            if model_path not in self._fence_detectors:
                try:
                    self._fence_detectors[model_path] = FenceDetector(model_path=model_path)
                except RuntimeError as exc:
                    self._fence_detectors[model_path] = None
                    self._fence_detector_errors[model_path] = str(exc)
            detector = self._fence_detectors[model_path]
            if detector is None:
                error = self._fence_detector_errors.get(model_path, "fence model unavailable")
                return None, error
            return detector, None


_MODEL_CACHE = _ModelCache()


def run_pipeline(image_path: Path, options: PipelineOptions | None = None) -> PipelineResult:
    """Run detection + fence segmentation + horizon estimation on one image.

    `image_path` must point at a real file on disk (EXIF reading needs a
    path, not just decoded pixels), same as detect.py's CLI usage.
    """
    options = options or PipelineOptions()
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"could not read image: {image_path}")
    height, width = image.shape[:2]

    is_open_vocab_model = "world" in options.model.lower()
    if options.classes:
        classes = list(options.classes)
    elif is_open_vocab_model:
        classes = DEFAULT_CITY_CLASSES
    else:
        classes = None

    detector = _MODEL_CACHE.get_detector(
        options.model, options.confidence, tuple(classes) if classes else None
    )
    detections = detector.detect(str(image_path))

    # Fence detection is required (see module docstring): failures raise
    # rather than falling back to a YOLO-only result.
    if not options.fence_model:
        raise FenceDetectionError("fence detection is required but no fence model was configured")

    fence_detector, error = _MODEL_CACHE.get_fence_detector(options.fence_model)
    if fence_detector is None:
        raise FenceDetectionError(f"fence detection model unavailable: {error}")

    try:
        fence_mask = fence_detector.predict_mask(image)
    except Exception as exc:
        raise FenceDetectionError(f"fence detection inference failed: {exc}") from exc

    fence_detections = mask_to_detections(
        fence_mask, threshold=fence_detector.confidence_threshold, min_area=fence_detector.min_area
    )
    detections = merge_detections(detections, fence_detections)

    camera = read_camera_metadata(image_path)
    effective_lens_mode = camera.lens_mode if options.lens_mode == "auto" else options.lens_mode
    distortion: DistortionSpec | None = None
    if options.curve_strength is not None:
        distortion = DistortionSpec(
            source="manual_curve_strength",
            curve_strength=options.curve_strength,
            is_approximation=True,
            basis="--curve-strength",
        )
    elif effective_lens_mode == "ultrawide":
        if options.lens_mode == "auto":
            if camera.focal_length_35mm is not None:
                basis = f"EXIF focal_length_35mm={camera.focal_length_35mm:g}"
            elif camera.lens_model:
                basis = f"EXIF lens_model={camera.lens_model}"
            else:
                basis = "EXIF ultrawide hint"
            distortion = generic_ultrawide_distortion("exif_heuristic", basis=basis)
        else:
            distortion = generic_ultrawide_distortion("manual_lens_mode", basis="--lens-mode ultrawide")

    horizon = estimate_horizon(image, distortion=distortion) if options.enable_horizon else None

    annotated = draw_detections(image, detections)
    if horizon is not None:
        annotated = draw_horizon(annotated, horizon)

    result = build_result(image_path.name, width, height, detections)
    camera_data = camera.to_dict()
    camera_data["lens_mode_effective"] = effective_lens_mode
    camera_data["lens_mode_source"] = "exif" if options.lens_mode == "auto" else "manual"
    result["image"]["camera"] = camera_data
    if horizon is not None:
        result["scene_geometry"] = {"horizon": horizon.to_dict()}

    return PipelineResult(
        result=result,
        annotated_image=annotated,
        detections=detections,
        horizon=horizon,
        fence_mask=fence_mask,
    )
