"""Tests for detect.py's CLI error handling around the now-mandatory fence
detection step. detect.py itself does not implement fence detection or any
YOLO-only fallback -- it just needs to turn a FenceDetectionError from
src.pipeline.run_pipeline() into a clean SystemExit, same as it already does
for ValueError (bad image path), rather than letting the exception crash
with a raw traceback.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import detect
from src.pipeline import FenceDetectionError


def test_main_exits_cleanly_when_fence_detection_unavailable(tmp_path, monkeypatch):
    image_path = tmp_path / "photo.jpg"
    image_path.write_bytes(b"not a real image, run_pipeline is stubbed below")
    output_dir = tmp_path / "output"

    def _raise_fence_error(image_path, options=None):
        raise FenceDetectionError("fence detection model unavailable: huggingface.co blocked")

    monkeypatch.setattr(detect, "run_pipeline", _raise_fence_error)
    monkeypatch.setattr(
        sys,
        "argv",
        ["detect.py", "--image", str(image_path), "--output-dir", str(output_dir)],
    )

    with pytest.raises(SystemExit) as exc_info:
        detect.main()

    assert "fence detection" in str(exc_info.value).lower()
