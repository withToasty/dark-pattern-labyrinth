"""Tests for the web/app.py FastAPI MVP (Issue #14).

These exercise only the web layer (upload validation, response shape, asset
retrieval, JSON/YAML retrieval). The actual recognition pipeline
(src/pipeline.run_pipeline) is monkeypatched so tests don't need to load
YOLO/SegFormer weights.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import src.pipeline as pipeline_module
import web.app as web_app
from src.detector import Detection
from src.export import build_result
from src.pipeline import PipelineResult

FAKE_HORIZON = {
    "detected": True,
    "method": "vertical_guided_single_vp",
    "role": "musical_reference",
    "confidence": 0.81,
    "candidate_detected": True,
    "reference_score": 0.76,
    "spatial_support_span": 0.68,
    "spatial_support_bins": 3,
    "in_frame_fraction": 1.0,
    "rejection_reason": None,
    "supporting_lines": 14,
    "orientation_source": None,
    "vanishing_points": None,
    "vertical_vanishing_point": None,
    "rectified": {
        "type": "line",
        "center_y": 24.0,
        "center_y_normalized": 0.5,
        "left_y": 22.0,
        "right_y": 26.0,
        "slope": 0.01,
        "angle_deg": 0.5,
    },
    "distorted": None,
}


def _valid_image_bytes(fmt: str = "JPEG") -> bytes:
    image = Image.new("RGB", (64, 48), color=(10, 20, 30))
    buf = io.BytesIO()
    image.save(buf, format=fmt)
    return buf.getvalue()


def _make_result_dict(detections: list[Detection], horizon_dict: dict | None) -> dict:
    result = build_result("original.jpg", 64, 48, detections)
    result["image"]["camera"] = {
        "make": None,
        "model": None,
        "lens_model": None,
        "focal_length_mm": None,
        "focal_length_35mm": None,
        "orientation": None,
        "lens_mode": "unknown",
        "lens_mode_effective": "unknown",
        "lens_mode_source": "exif",
    }
    if horizon_dict is not None:
        result["scene_geometry"] = {"horizon": horizon_dict}
    return result


def _fake_run_pipeline(with_fence: bool = False, with_horizon: bool = True, warnings: list[str] | None = None):
    def _run(image_path, options=None):
        detections = [Detection(id=1, label="car", confidence=0.87, minx=10, maxx=50, miny=5, maxy=40)]
        fence_mask = None
        if with_fence:
            fence_mask = np.zeros((48, 64), dtype=np.float32)
            fence_mask[10:20, 10:20] = 0.9
            detections.append(Detection(id=2, label="fence", confidence=0.9, minx=10, maxx=20, miny=10, maxy=20))
        result = _make_result_dict(detections, FAKE_HORIZON if with_horizon else None)
        annotated = np.full((48, 64, 3), 128, dtype=np.uint8)
        return PipelineResult(
            result=result,
            annotated_image=annotated,
            detections=detections,
            horizon=None,
            fence_mask=fence_mask,
            warnings=warnings or [],
        )

    return _run


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(web_app, "RUNS_DIR", tmp_path / "runs")
    monkeypatch.setattr(web_app, "run_pipeline", _fake_run_pipeline())
    return TestClient(web_app.app)


def test_analyze_success_returns_expected_shape(client):
    files = {"image": ("photo.jpg", _valid_image_bytes("JPEG"), "image/jpeg")}
    response = client.post("/api/analyze", files=files)

    assert response.status_code == 200
    data = response.json()

    assert set(["run_id", "result", "json_text", "yaml_text", "warnings", "assets"]) <= set(data.keys())
    assert data["run_id"]
    assert data["result"]["detections"][0]["label"] == "car"
    assert data["result"]["scene_geometry"]["horizon"]["detected"] is True
    assert data["warnings"] == []
    assert "\"detections\"" in data["json_text"]
    assert "detections:" in data["yaml_text"]

    assets = data["assets"]
    for key in ("original", "annotated", "json", "yaml"):
        assert assets[key] == f"/api/runs/{data['run_id']}/{key}"
    assert assets["fence_mask"] is None


def test_analyze_with_fence_mask_exposes_asset_url(tmp_path, monkeypatch):
    monkeypatch.setattr(web_app, "RUNS_DIR", tmp_path / "runs")
    monkeypatch.setattr(web_app, "run_pipeline", _fake_run_pipeline(with_fence=True))
    client = TestClient(web_app.app)

    files = {"image": ("photo.png", _valid_image_bytes("PNG"), "image/png")}
    response = client.post("/api/analyze", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["assets"]["fence_mask"] == f"/api/runs/{data['run_id']}/fence_mask"

    mask_response = client.get(data["assets"]["fence_mask"])
    assert mask_response.status_code == 200
    assert mask_response.headers["content-type"] in ("image/png", "application/octet-stream")


def test_analyze_reports_warnings(tmp_path, monkeypatch):
    # Non-fatal warnings (unrelated to fence detection, which is required --
    # see the FenceDetectionError tests below) should still pass through.
    monkeypatch.setattr(web_app, "RUNS_DIR", tmp_path / "runs")
    monkeypatch.setattr(
        web_app,
        "run_pipeline",
        _fake_run_pipeline(warnings=["example non-fatal notice for downstream consumers"]),
    )
    client = TestClient(web_app.app)

    files = {"image": ("photo.jpg", _valid_image_bytes("JPEG"), "image/jpeg")}
    response = client.post("/api/analyze", files=files)

    assert response.status_code == 200
    assert len(response.json()["warnings"]) == 1


class _StubObjectDetector:
    """Stands in for ObjectDetector so these tests don't need ultralytics."""

    def detect(self, image_path):
        return [Detection(id=1, label="car", confidence=0.9, minx=1, maxx=10, miny=1, maxy=10)]


class _FailingFenceDetector:
    confidence_threshold = 0.5
    min_area = 500

    def predict_mask(self, image):
        raise RuntimeError("segformer inference blew up")


def test_analyze_fails_when_fence_model_unavailable(tmp_path, monkeypatch):
    """Fence detection is required: a load failure must not be reported as
    a successful YOLO-only analysis. It exercises the real run_pipeline
    (not the web-level fake), with only the model cache mocked."""
    monkeypatch.setattr(web_app, "RUNS_DIR", tmp_path / "runs")
    monkeypatch.setattr(pipeline_module._MODEL_CACHE, "get_detector", lambda *a, **k: _StubObjectDetector())
    monkeypatch.setattr(
        pipeline_module._MODEL_CACHE,
        "get_fence_detector",
        lambda *a, **k: (None, "could not load fence model: huggingface.co blocked"),
    )
    client = TestClient(web_app.app)

    files = {"image": ("photo.jpg", _valid_image_bytes("JPEG"), "image/jpeg")}
    response = client.post("/api/analyze", files=files)

    assert response.status_code == 503
    detail = response.json()["detail"]
    assert "fence detection" in detail.lower()
    assert "Traceback" not in detail


def test_analyze_fails_when_fence_inference_raises(tmp_path, monkeypatch):
    """Fence detection is required: an inference-time failure must not
    silently degrade to a YOLO-only success either."""
    monkeypatch.setattr(web_app, "RUNS_DIR", tmp_path / "runs")
    monkeypatch.setattr(pipeline_module._MODEL_CACHE, "get_detector", lambda *a, **k: _StubObjectDetector())
    monkeypatch.setattr(
        pipeline_module._MODEL_CACHE,
        "get_fence_detector",
        lambda *a, **k: (_FailingFenceDetector(), None),
    )
    client = TestClient(web_app.app)

    files = {"image": ("photo.jpg", _valid_image_bytes("JPEG"), "image/jpeg")}
    response = client.post("/api/analyze", files=files)

    assert response.status_code == 503
    detail = response.json()["detail"]
    assert "fence detection" in detail.lower()
    assert "Traceback" not in detail


def test_analyze_rejects_unsupported_extension(client):
    files = {"image": ("notes.txt", b"just some text", "text/plain")}
    response = client.post("/api/analyze", files=files)

    assert response.status_code == 400
    assert "unsupported file type" in response.json()["detail"]


def test_analyze_rejects_corrupt_image_bytes(client):
    files = {"image": ("photo.jpg", b"this is not a real jpeg", "image/jpeg")}
    response = client.post("/api/analyze", files=files)

    assert response.status_code == 400
    assert "could not read image" in response.json()["detail"]


def test_analyze_rejects_empty_file(client):
    files = {"image": ("photo.jpg", b"", "image/jpeg")}
    response = client.post("/api/analyze", files=files)

    assert response.status_code == 400


def test_get_original_and_annotated_assets(client):
    files = {"image": ("photo.jpg", _valid_image_bytes("JPEG"), "image/jpeg")}
    run_id = client.post("/api/analyze", files=files).json()["run_id"]

    original = client.get(f"/api/runs/{run_id}/original")
    annotated = client.get(f"/api/runs/{run_id}/annotated")

    assert original.status_code == 200
    assert annotated.status_code == 200
    assert len(annotated.content) > 0


def test_get_json_and_yaml_assets_match_inline_text(client):
    files = {"image": ("photo.jpg", _valid_image_bytes("JPEG"), "image/jpeg")}
    data = client.post("/api/analyze", files=files).json()
    run_id = data["run_id"]

    json_response = client.get(f"/api/runs/{run_id}/json")
    yaml_response = client.get(f"/api/runs/{run_id}/yaml")

    assert json_response.status_code == 200
    assert yaml_response.status_code == 200
    assert json_response.text == data["json_text"]
    assert yaml_response.text == data["yaml_text"]


def test_unknown_run_id_returns_404(client):
    response = client.get("/api/runs/does-not-exist/original")
    assert response.status_code == 404


def test_path_traversal_run_id_returns_404(client):
    response = client.get("/api/runs/..%2F..%2Fetc/original")
    assert response.status_code in (404, 422)
