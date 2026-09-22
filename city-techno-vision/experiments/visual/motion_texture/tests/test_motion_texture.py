"""Tests for the Motion Texture MVP.

Uses small NumPy-generated pseudo frames and a temporary synthetic video
(written with cv2.VideoWriter) instead of committing real video fixtures.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from motion_texture import (
    build_depth_proxy,
    composite_motion_texture,
    read_video_frames,
    render_motion_texture,
    resolve_direction,
    sample_frame_indices,
)


def _make_frame(height: int, width: int, fill: int) -> np.ndarray:
    return np.full((height, width, 3), fill, dtype=np.uint8)


def _make_gradient_frame(height: int, width: int, offset: int) -> np.ndarray:
    """A frame with horizontal variation, so horizontal warps are visible."""
    columns = (np.arange(width, dtype=np.int32) + offset) % 256
    row = columns.astype(np.uint8)
    frame = np.tile(row.reshape(1, width, 1), (height, 1, 3))
    return frame


def _make_pseudo_frames(count: int = 6, height: int = 20, width: int = 16) -> list[np.ndarray]:
    return [_make_frame(height, width, fill=(i * 30) % 255) for i in range(count)]


def _make_gradient_pseudo_frames(count: int = 6, height: int = 20, width: int = 16) -> list[np.ndarray]:
    return [_make_gradient_frame(height, width, offset=i * 3) for i in range(count)]


def _write_synthetic_video(path: Path, count: int = 8, height: int = 24, width: int = 32) -> Path:
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    writer = cv2.VideoWriter(str(path), fourcc, 10, (width, height))
    for i in range(count):
        writer.write(_make_frame(height, width, fill=(i * 25) % 255))
    writer.release()
    return path


# --- frame sampling ---------------------------------------------------


def test_sample_frame_indices_spans_full_range():
    indices = sample_frame_indices(total_frames=100, num_samples=5)
    assert len(indices) == 5
    assert indices[0] == 0
    assert indices[-1] == 99
    assert indices == sorted(indices)


def test_sample_frame_indices_rejects_too_few_samples():
    with pytest.raises(ValueError):
        sample_frame_indices(total_frames=10, num_samples=1)


# --- depth proxy --------------------------------------------------------


def test_depth_proxy_is_zero_at_horizon_and_one_at_bottom():
    depth = build_depth_proxy(height=10, width=4, horizon_y=0.5)
    assert depth.shape == (10, 4)
    horizon_row = int(round(0.5 * 9))
    assert depth[horizon_row, 0] == pytest.approx(0.0, abs=1e-3)
    assert depth[-1, 0] == pytest.approx(1.0, abs=1e-3)
    # Monotonically non-decreasing from horizon to bottom.
    column = depth[horizon_row:, 0]
    assert np.all(np.diff(column) >= 0)


def test_depth_proxy_rejects_out_of_range_horizon():
    with pytest.raises(ValueError):
        build_depth_proxy(height=10, width=4, horizon_y=1.5)


# --- direction resolution -----------------------------------------------


def test_resolve_direction_explicit_values():
    assert resolve_direction("left", seed=0) == -1
    assert resolve_direction("right", seed=0) == 1


def test_resolve_direction_auto_is_deterministic_for_seed():
    assert resolve_direction("auto", seed=2) == resolve_direction("auto", seed=2)


def test_resolve_direction_rejects_invalid_value():
    with pytest.raises(ValueError):
        resolve_direction("sideways", seed=0)


# --- compositing: determinism + output size ------------------------------


def test_composite_is_deterministic_given_same_seed():
    frames = _make_pseudo_frames()
    image_a, direction_a = composite_motion_texture(frames, horizon_y=0.5, strength=10.0, direction="auto", seed=7)
    image_b, direction_b = composite_motion_texture(frames, horizon_y=0.5, strength=10.0, direction="auto", seed=7)
    assert direction_a == direction_b
    assert np.array_equal(image_a, image_b)


def test_composite_differs_across_seeds():
    frames = _make_gradient_pseudo_frames()
    image_a, _ = composite_motion_texture(frames, horizon_y=0.5, strength=25.0, direction="right", seed=1)
    image_b, _ = composite_motion_texture(frames, horizon_y=0.5, strength=25.0, direction="right", seed=2)
    assert not np.array_equal(image_a, image_b)


def test_composite_output_matches_input_frame_size():
    frames = _make_pseudo_frames(height=20, width=16)
    image, _ = composite_motion_texture(frames, horizon_y=0.5, strength=10.0, direction="auto", seed=0)
    assert image.shape == (20, 16, 3)


def test_composite_requires_at_least_two_frames():
    with pytest.raises(ValueError):
        composite_motion_texture(_make_pseudo_frames(count=1), horizon_y=0.5, strength=10.0, direction="auto", seed=0)


# --- video reading (temporary synthetic video) ---------------------------


def test_read_video_frames_samples_requested_count(tmp_path):
    video_path = _write_synthetic_video(tmp_path / "clip.avi")
    frames = read_video_frames(video_path, num_frames=4)
    assert len(frames) == 4


def test_read_video_frames_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_video_frames(tmp_path / "missing.mp4", num_frames=4)


# --- full pipeline: metadata JSON + invalid input -------------------------


def test_render_motion_texture_writes_png_and_metadata(tmp_path):
    video_path = _write_synthetic_video(tmp_path / "clip.avi")
    output_dir = tmp_path / "out"

    image_path, metadata_path = render_motion_texture(
        video_path=video_path,
        output_dir=output_dir,
        frames=5,
        horizon_y=0.6,
        strength=15.0,
        direction="left",
        seed=3,
    )

    assert image_path.exists()
    assert metadata_path.exists()

    loaded = cv2.imread(str(image_path))
    assert loaded is not None
    assert loaded.shape[:2] == (24, 32)

    metadata = json.loads(metadata_path.read_text())
    for key in (
        "video",
        "frames_requested",
        "frames_used",
        "horizon_y",
        "strength",
        "direction",
        "resolved_direction",
        "seed",
        "output_width",
        "output_height",
    ):
        assert key in metadata
    assert metadata["direction"] == "left"
    assert metadata["resolved_direction"] == "left"
    assert metadata["seed"] == 3


def test_render_motion_texture_invalid_video_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        render_motion_texture(video_path=tmp_path / "nope.mp4", output_dir=tmp_path / "out")


def test_render_motion_texture_invalid_direction_raises(tmp_path):
    video_path = _write_synthetic_video(tmp_path / "clip.avi")
    with pytest.raises(ValueError):
        render_motion_texture(video_path=video_path, output_dir=tmp_path / "out", direction="up")
