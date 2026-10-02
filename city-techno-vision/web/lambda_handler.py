"""AWS Lambda handler exposing city-techno-vision's detection pipeline over HTTP.

POST /detect with a JSON body:

  {
    "image_base64": "<base64-encoded image bytes>",
    "enable_fence": true,     # optional, default true
    "enable_horizon": true,   # optional, default true
    "conf": 0.15              # optional, default 0.15
  }

Response body:

  {
    "result": { ... same shape as detect.py's detections.json ... },
    "annotated_image_base64": "<base64-encoded JPEG>"
  }

Turning these results into sound is a separate project and does not belong here.
"""

from __future__ import annotations

import base64
import binascii
import json
import os
import tempfile
from pathlib import Path

import cv2
import numpy as np

from src.camera_metadata import read_camera_metadata
from src.detector import ObjectDetector, merge_detections
from src.export import build_result
from src.fence_detector import DEFAULT_FENCE_MODEL_ID, FenceDetector, mask_to_detections
from src.horizon import estimate_horizon
from src.visualize import draw_detections, draw_horizon

YOLO_MODEL_PATH = os.environ.get("YOLO_MODEL_PATH", "yolov8n-oiv7.pt")
FENCE_MODEL_ID = os.environ.get("FENCE_MODEL_ID", DEFAULT_FENCE_MODEL_ID)
DEFAULT_CONF = float(os.environ.get("CONF_THRESHOLD", "0.15"))

# Loaded lazily and kept warm across invocations that reuse the same container.
_detector: ObjectDetector | None = None
_fence_detector: FenceDetector | None | bool = None


def _get_detector(conf: float) -> ObjectDetector:
    global _detector
    if _detector is None or _detector.confidence_threshold != conf:
        _detector = ObjectDetector(model_path=YOLO_MODEL_PATH, confidence_threshold=conf, classes=None)
    return _detector


def _get_fence_detector() -> FenceDetector | None:
    global _fence_detector
    if _fence_detector is None:
        try:
            _fence_detector = FenceDetector(model_path=FENCE_MODEL_ID)
        except RuntimeError as exc:
            print(f"warning: fence detection unavailable: {exc}")
            _fence_detector = False
    return _fence_detector or None


def _response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body, ensure_ascii=False),
    }


def handler(event, context):
    try:
        raw_body = event.get("body") or "{}"
        if event.get("isBase64Encoded"):
            raw_body = base64.b64decode(raw_body).decode("utf-8")
        payload = json.loads(raw_body)
    except (json.JSONDecodeError, binascii.Error, UnicodeDecodeError):
        return _response(400, {"error": "invalid JSON body"})

    image_b64 = payload.get("image_base64")
    if not image_b64:
        return _response(400, {"error": "image_base64 is required"})

    try:
        image_bytes = base64.b64decode(image_b64)
    except binascii.Error:
        return _response(400, {"error": "image_base64 is not valid base64"})

    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image is None:
        return _response(400, {"error": "could not decode image"})
    height, width = image.shape[:2]

    conf = float(payload.get("conf", DEFAULT_CONF))
    enable_fence = bool(payload.get("enable_fence", True))
    enable_horizon = bool(payload.get("enable_horizon", True))

    # /tmp is the only writable path in a Lambda execution environment; EXIF
    # reading and Ultralytics both want a real file path, not an in-memory buffer.
    with tempfile.NamedTemporaryFile(suffix=".jpg", dir="/tmp") as tmp:
        tmp.write(image_bytes)
        tmp.flush()
        detector = _get_detector(conf)
        detections = detector.detect(tmp.name)
        camera = read_camera_metadata(Path(tmp.name))

    if enable_fence:
        fence_detector = _get_fence_detector()
        if fence_detector is not None:
            fence_mask = fence_detector.predict_mask(image)
            fence_detections = mask_to_detections(
                fence_mask, threshold=fence_detector.confidence_threshold, min_area=fence_detector.min_area
            )
            detections = merge_detections(detections, fence_detections)

    horizon = estimate_horizon(image) if enable_horizon else None

    annotated = draw_detections(image, detections)
    if horizon is not None:
        annotated = draw_horizon(annotated, horizon)
    ok, encoded = cv2.imencode(".jpg", annotated)
    annotated_b64 = base64.b64encode(encoded.tobytes()).decode("ascii") if ok else None

    result = build_result(payload.get("filename", "upload.jpg"), width, height, detections)
    camera_data = camera.to_dict()
    camera_data["lens_mode_effective"] = camera.lens_mode
    camera_data["lens_mode_source"] = "exif"
    result["image"]["camera"] = camera_data
    if horizon is not None:
        result["scene_geometry"] = {"horizon": horizon.to_dict()}

    return _response(200, {"result": result, "annotated_image_base64": annotated_b64})
