"""Tests for camera metadata lens-mode inference."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.camera_metadata import infer_lens_mode


def test_ultrawide_detected_from_35mm_equivalent():
    assert infer_lens_mode(None, 13.0) == "ultrawide"


def test_ultrawide_detected_from_lens_name():
    assert infer_lens_mode("iPhone Ultra Wide Camera", None) == "ultrawide"


def test_standard_lens_from_35mm_equivalent():
    assert infer_lens_mode(None, 24.0) == "standard"


def test_unknown_without_lens_hints():
    assert infer_lens_mode(None, None) == "unknown"
