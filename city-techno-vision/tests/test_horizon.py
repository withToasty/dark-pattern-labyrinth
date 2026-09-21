"""Offline tests for geometric horizon estimation."""

import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.horizon import estimate_horizon


def _synthetic_perspective_scene() -> np.ndarray:
    height, width = 600, 800
    image = np.zeros((height, width, 3), dtype=np.uint8)
    left_vp = np.array([-500.0, 280.0])
    right_vp = np.array([1300.0, 320.0])
    anchors = [
        (100, 500),
        (200, 420),
        (300, 520),
        (500, 460),
        (650, 520),
        (700, 400),
    ]

    for vanishing_point in (left_vp, right_vp):
        for anchor_x, anchor_y in anchors:
            anchor = np.array([anchor_x, anchor_y], dtype=float)
            direction = vanishing_point - anchor
            direction /= np.linalg.norm(direction)
            start = anchor - 100 * direction
            end = anchor + 100 * direction
            cv2.line(
                image,
                tuple(np.round(start).astype(int)),
                tuple(np.round(end).astype(int)),
                (255, 255, 255),
                3,
            )
    return image


def _synthetic_urban_scene() -> np.ndarray:
    height, width = 600, 800
    image = np.zeros((height, width, 3), dtype=np.uint8)

    for x in (80, 140, 220, 300, 500, 580, 660, 730):
        cv2.line(image, (x, 150), (x, 520), (255, 255, 255), 3)

    horizontal_vp = np.array([-900.0, 300.0])
    anchors = [
        (120, 520),
        (220, 470),
        (340, 540),
        (460, 490),
        (620, 530),
        (720, 450),
    ]
    for anchor_x, anchor_y in anchors:
        anchor = np.array([anchor_x, anchor_y], dtype=float)
        direction = horizontal_vp - anchor
        direction /= np.linalg.norm(direction)
        start = anchor - 120 * direction
        end = anchor + 120 * direction
        cv2.line(
            image,
            tuple(np.round(start).astype(int)),
            tuple(np.round(end).astype(int)),
            (255, 255, 255),
            3,
        )

    return image


def test_estimate_horizon_finds_expected_line():
    result = estimate_horizon(_synthetic_perspective_scene())

    assert result.detected
    assert result.confidence >= 0.5
    assert result.left_y is not None
    assert result.right_y is not None
    assert result.center_y is not None
    assert 285 <= result.left_y <= 300
    assert 300 <= result.right_y <= 315
    assert 295 <= result.center_y <= 305
    assert result.slope is not None and 0.0 < result.slope < 0.04
    assert result.supporting_lines >= 6
    assert result.vanishing_points is not None
    assert len(result.vanishing_points) == 2


def test_vertical_guided_method_needs_only_one_horizontal_vanishing_point():
    result = estimate_horizon(_synthetic_urban_scene())

    assert result.detected
    assert result.method == "vertical_guided_single_vp"
    assert result.confidence >= 0.5
    assert result.center_y is not None
    assert 280 <= result.center_y <= 320
    assert result.slope is not None
    assert abs(result.slope) < 0.02
    assert result.vanishing_points is not None
    assert len(result.vanishing_points) == 1


def test_estimate_horizon_returns_not_detected_for_blank_image():
    blank = np.zeros((400, 600, 3), dtype=np.uint8)

    result = estimate_horizon(blank)

    assert not result.detected
    assert result.confidence == 0.0
