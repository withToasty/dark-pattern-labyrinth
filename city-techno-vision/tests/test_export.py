"""Tests for exported semantic groups."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.detector import Detection
from src.export import build_result


def _det(label: str) -> Detection:
    return Detection(
        id=1,
        label=label,
        confidence=0.5,
        minx=0,
        maxx=10,
        miny=0,
        maxy=10,
    )


def test_car_and_land_vehicle_share_road_vehicle_group():
    result = build_result(
        "sample.jpg",
        100,
        100,
        [_det("Car"), _det("Land vehicle")],
    )

    assert result["detections"][0]["group"] == "road_vehicle"
    assert result["detections"][1]["group"] == "road_vehicle"
    assert result["detections"][0]["label"] == "Car"
    assert result["detections"][1]["label"] == "Land vehicle"


def test_non_vehicle_label_keeps_raw_schema_without_group():
    result = build_result("sample.jpg", 100, 100, [_det("Tree")])

    assert result["detections"][0]["label"] == "Tree"
    assert "group" not in result["detections"][0]
