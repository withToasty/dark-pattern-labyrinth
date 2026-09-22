"""Tests for src/pipeline.py's "always run all three steps" contract.

A normal successful run_pipeline() call always runs YOLO detection,
SegFormer fence detection, and horizon estimation together -- there is no
option to skip any of them. These tests exercise the real run_pipeline with
only the model cache mocked (ObjectDetector/FenceDetector stand-ins), so no
real weights are loaded. There is no YOLO-only fallback to test -- that's
the point: any fence failure must raise FenceDetectionError.
"""

from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import src.pipeline as pipeline_module
from src.detector import Detection
from src.pipeline import FenceDetectionError, PipelineOptions, run_pipeline


class _StubObjectDetector:
    def detect(self, image_path):
        return [Detection(id=1, label="car", confidence=0.9, minx=1, maxx=10, miny=1, maxy=10)]


class _StubFenceDetector:
    confidence_threshold = 0.5
    min_area = 500

    def __init__(self, mask):
        self._mask = mask

    def predict_mask(self, image):
        return self._mask


class _FailingFenceDetector:
    confidence_threshold = 0.5
    min_area = 500

    def predict_mask(self, image):
        raise RuntimeError("segformer inference blew up")


@pytest.fixture
def sample_image(tmp_path) -> Path:
    image_path = tmp_path / "sample.jpg"
    cv2.imwrite(str(image_path), np.zeros((120, 200, 3), dtype=np.uint8))
    return image_path


@pytest.fixture(autouse=True)
def _stub_object_detector(monkeypatch):
    # Every test here cares about fence behavior, not YOLO itself.
    monkeypatch.setattr(pipeline_module._MODEL_CACHE, "get_detector", lambda *a, **k: _StubObjectDetector())


def test_run_pipeline_raises_when_fence_model_unavailable(sample_image, monkeypatch):
    monkeypatch.setattr(
        pipeline_module._MODEL_CACHE,
        "get_fence_detector",
        lambda *a, **k: (None, "could not load fence model: huggingface.co blocked"),
    )

    with pytest.raises(FenceDetectionError, match="fence detection"):
        run_pipeline(sample_image, PipelineOptions())


def test_run_pipeline_raises_when_fence_inference_fails(sample_image, monkeypatch):
    monkeypatch.setattr(
        pipeline_module._MODEL_CACHE,
        "get_fence_detector",
        lambda *a, **k: (_FailingFenceDetector(), None),
    )

    with pytest.raises(FenceDetectionError, match="fence detection"):
        run_pipeline(sample_image, PipelineOptions())


def test_run_pipeline_raises_when_no_fence_model_configured(sample_image):
    with pytest.raises(FenceDetectionError, match="fence detection"):
        run_pipeline(sample_image, PipelineOptions(fence_model=None))


def test_run_pipeline_succeeds_with_yolo_fence_and_horizon(sample_image, monkeypatch):
    fence_mask = np.zeros((120, 200), dtype=np.float32)
    fence_mask[10:40, 20:150] = 0.9
    monkeypatch.setattr(
        pipeline_module._MODEL_CACHE,
        "get_fence_detector",
        lambda *a, **k: (_StubFenceDetector(fence_mask), None),
    )

    result = run_pipeline(sample_image, PipelineOptions())

    labels = {det.label for det in result.detections}
    assert "car" in labels
    assert "fence" in labels
    assert result.fence_mask is not None
    # Horizon estimation always runs and produces a result either way; a
    # `detected: false` outcome (likely here, on a blank synthetic image)
    # is still a normal, successful result, not an error.
    assert result.horizon is not None
    assert "scene_geometry" in result.result
    assert result.result["scene_geometry"]["horizon"]["detected"] in (True, False)
