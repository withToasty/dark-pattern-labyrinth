"""Draw bounding boxes, labels, and confidence scores onto an image."""

from __future__ import annotations

import cv2
import numpy as np

from .detector import Detection

BOX_COLOR = (46, 204, 113)  # BGR
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
