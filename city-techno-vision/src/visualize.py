"""Draw bounding boxes, labels, confidence scores, and scene geometry."""

from __future__ import annotations

import cv2
import numpy as np

from .detector import Detection
from .horizon import HorizonResult

BOX_COLOR = (46, 204, 113)  # BGR
HORIZON_COLOR = (0, 215, 255)
DISTORTED_HORIZON_COLOR = (255, 0, 255)
TEXT_COLOR = (12, 20, 12)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
BOX_THICKNESS = 2


def draw_detections(image: np.ndarray, detections: list[Detection]) -> np.ndarray:
    """Return a copy of `image` with each detection's box and label drawn on it."""
    annotated = image.copy()
    for det in detections:
        top_left = (det.minx, det.miny)
        bottom_right = (det.maxx, det.maxy)
        cv2.rectangle(annotated, top_left, bottom_right, BOX_COLOR, BOX_THICKNESS)
        _draw_label(annotated, det)
    return annotated


def draw_horizon(image: np.ndarray, horizon: HorizonResult) -> np.ndarray:
    """Return a copy with the rectified (straight) and distorted (curved) horizon drawn on it."""
    annotated = image.copy()
    if not horizon.detected or horizon.left_y is None or horizon.right_y is None:
        return annotated

    height, width = annotated.shape[:2]
    left = (0, int(round(horizon.left_y)))
    right = (width - 1, int(round(horizon.right_y)))
    cv2.line(annotated, left, right, HORIZON_COLOR, 2, cv2.LINE_AA)

    distorted = horizon.distorted_dict()
    if distorted is not None:
        polyline = np.array(
            [[int(round(x)), int(round(y))] for x, y in distorted["points"]],
            dtype=np.int32,
        )
        cv2.polylines(
            annotated, [polyline], isClosed=False, color=DISTORTED_HORIZON_COLOR, thickness=2, lineType=cv2.LINE_AA
        )

    label_y = int(round(horizon.center_y or height / 2))
    label_y = min(max(label_y - 8, 18), height - 6)
    label = f"horizon {horizon.confidence:.2f}"
    cv2.putText(
        annotated,
        label,
        (8, label_y),
        FONT,
        FONT_SCALE,
        HORIZON_COLOR,
        2,
        cv2.LINE_AA,
    )
    return annotated


def _draw_label(image: np.ndarray, det: Detection) -> None:
    text = f"{det.label} {det.confidence:.2f}"
    (text_w, text_h), baseline = cv2.getTextSize(text, FONT, FONT_SCALE, 1)

    label_top = max(0, det.miny - text_h - baseline - 4)
    cv2.rectangle(
        image,
        (det.minx, label_top),
        (det.minx + text_w + 4, label_top + text_h + baseline + 4),
        BOX_COLOR,
        -1,
    )
    cv2.putText(
        image,
        text,
        (det.minx + 2, label_top + text_h + 2),
        FONT,
        FONT_SCALE,
        TEXT_COLOR,
        1,
        cv2.LINE_AA,
    )
