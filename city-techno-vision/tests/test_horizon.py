"""Offline tests for geometric horizon estimation."""

import sys
from pathlib import Path

import cv2
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.horizon import (
    HorizonResult,
    _apply_reference_gate,
    estimate_horizon,
    generic_ultrawide_distortion,
)


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



def _synthetic_vertical_vp_scene() -> np.ndarray:
    height, width = 600, 800
    image = np.zeros((height, width, 3), dtype=np.uint8)

    vertical_vp = np.array([430.0, -1400.0])
    vertical_anchors = [
        (70, 520),
        (150, 480),
        (240, 540),
        (330, 500),
        (470, 520),
        (560, 470),
        (650, 540),
        (730, 500),
    ]
    for anchor_x, anchor_y in vertical_anchors:
        anchor = np.array([anchor_x, anchor_y], dtype=float)
        direction = vertical_vp - anchor
        direction /= np.linalg.norm(direction)
        start = anchor - 110 * direction
        end = anchor + 110 * direction
        cv2.line(
            image,
            tuple(np.round(start).astype(int)),
            tuple(np.round(end).astype(int)),
            (255, 255, 255),
            3,
        )

    horizontal_vp = np.array([-900.0, 300.0])
    horizontal_anchors = [
        (120, 520),
        (220, 470),
        (340, 540),
        (460, 490),
        (620, 530),
        (720, 450),
    ]
    for anchor_x, anchor_y in horizontal_anchors:
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



def test_vertical_vanishing_point_drives_roll_in_wide_angle_like_scene():
    result = estimate_horizon(_synthetic_vertical_vp_scene())

    assert result.detected
    assert result.method == "vertical_guided_single_vp"
    assert result.orientation_source == "vertical_vanishing_point"
    assert result.vertical_vanishing_point is not None
    assert result.vertical_vanishing_point.supporting_lines >= 4
    assert result.angle_deg is not None
    assert 0.2 <= result.angle_deg <= 2.0

    data = result.to_dict()
    assert data["orientation_source"] == "vertical_vanishing_point"
    assert data["vertical_vanishing_point"] is not None

def test_estimate_horizon_returns_not_detected_for_blank_image():
    blank = np.zeros((400, 600, 3), dtype=np.uint8)

    result = estimate_horizon(blank)

    assert not result.detected
    assert result.confidence == 0.0


def test_to_dict_splits_rectified_line_and_distorted_curve():
    result = estimate_horizon(
        _synthetic_urban_scene(),
        distortion=generic_ultrawide_distortion(
            "manual_lens_mode", basis="test ultrawide hint"
        ),
    )
    data = result.to_dict()

    assert "left_y" not in data
    assert data["role"] == "musical_reference"
    assert data["rectified"]["type"] == "line"
    assert data["rectified"]["center_y"] == pytest.approx(result.center_y, abs=1e-3)
    assert data["rectified"]["left_y"] == pytest.approx(result.left_y, abs=1e-3)
    assert data["rectified"]["right_y"] == pytest.approx(result.right_y, abs=1e-3)

    distorted = data["distorted"]
    assert distorted["type"] == "curve"
    assert distorted["sampling"] == "polyline"
    assert distorted["distortion_source"] == "manual_lens_mode"
    assert distorted["distortion_model"] == "parabolic_approximation"
    assert distorted["is_approximation"] is True
    assert distorted["basis"] == "test ultrawide hint"
    assert len(distorted["points"]) == 7
    # The curve matches the rectified line at the image's horizontal center.
    assert distorted["center_y"] == pytest.approx(result.center_y, abs=1e-3)
    center_index = len(distorted["points"]) // 2
    assert distorted["points"][center_index][1] == pytest.approx(result.center_y, abs=1e-3)
    # And bows away from it toward the left/right edges.
    assert distorted["points"][0][1] != pytest.approx(result.left_y, abs=1e-3)
    assert distorted["points"][-1][1] != pytest.approx(result.right_y, abs=1e-3)


def test_to_dict_has_no_rectified_or_distorted_when_not_detected():
    blank = np.zeros((400, 600, 3), dtype=np.uint8)
    result = estimate_horizon(blank)

    data = result.to_dict()

    assert data["rectified"] is None
    assert data["distorted"] is None


def test_to_dict_does_not_fake_curve_without_distortion_hint():
    result = estimate_horizon(_synthetic_urban_scene())
    data = result.to_dict()

    assert data["rectified"] is not None
    assert data["distorted"] is None


def _candidate_for_gate(
    *,
    angle_deg: float = 1.0,
    spatial_span: float = 0.7,
    spatial_bins: int = 3,
    left_y: float = 280.0,
    right_y: float = 290.0,
    confidence: float = 0.75,
) -> HorizonResult:
    slope = (right_y - left_y) / 799
    return HorizonResult(
        detected=True,
        method="test_candidate",
        confidence=confidence,
        left_y=left_y,
        right_y=right_y,
        center_y=(left_y + right_y) / 2,
        center_y_normalized=((left_y + right_y) / 2) / 600,
        slope=slope,
        angle_deg=angle_deg,
        spatial_support_span=spatial_span,
        spatial_support_bins=spatial_bins,
    )


def test_reference_gate_accepts_natural_musical_reference():
    result = _candidate_for_gate()

    _apply_reference_gate(result, 800, 600)

    assert result.detected
    assert result.candidate_detected
    assert result.rejection_reason is None
    assert result.reference_score >= 0.45


def test_reference_gate_rejects_localized_support():
    result = _candidate_for_gate(spatial_span=0.12, spatial_bins=1)

    _apply_reference_gate(result, 800, 600)

    assert not result.detected
    assert result.candidate_detected
    assert result.rejection_reason == "insufficient_spatial_support"


def test_reference_gate_rejects_visually_excessive_tilt():
    result = _candidate_for_gate(angle_deg=11.0)

    _apply_reference_gate(result, 800, 600)

    assert not result.detected
    assert result.rejection_reason == "excessive_tilt"


def test_reference_gate_rejects_mostly_out_of_frame():
    result = _candidate_for_gate(left_y=-300.0, right_y=100.0, angle_deg=1.0)

    _apply_reference_gate(result, 800, 600)

    assert not result.detected
    assert result.rejection_reason == "mostly_out_of_frame"
