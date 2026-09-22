"""Core algorithm for the Motion Texture MVP.

Compresses a short video into a single PNG where near rows (below the
horizon) accumulate a strong directional streak across sampled frames,
while far rows (near the horizon) stay close to the first frame.

Deliberately simple: sampling, depth proxy, warp, and blend are each a
small standalone function so the pipeline stays easy to follow.
"""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np

# Maximum per-pixel blend weight at the nearest row. Far rows (depth 0)
# always keep alpha 0, so they never drift from the first sampled frame.
BLEND_ALPHA_MAX = 0.65

VALID_DIRECTIONS = ("left", "right", "auto")


def sample_frame_indices(total_frames: int, num_samples: int) -> list[int]:
    """Return `num_samples` frame indices evenly spaced across the clip."""
    if total_frames <= 0:
        raise ValueError(f"total_frames must be positive, got {total_frames}")
    if num_samples < 2:
        raise ValueError(f"num_samples (--frames) must be at least 2, got {num_samples}")
    return [int(round(i)) for i in np.linspace(0, total_frames - 1, num_samples)]


def read_video_frames(video_path: str | Path, num_frames: int) -> list[np.ndarray]:
    """Read `num_frames` evenly-sampled BGR frames from a video file."""
    path = Path(video_path)
    if not path.exists():
        raise FileNotFoundError(f"video not found: {video_path}")

    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        cap.release()
        raise ValueError(f"could not open video: {video_path}")

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames: list[np.ndarray] = []
    try:
        if total > 0:
            for idx in sample_frame_indices(total, num_frames):
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ok, frame = cap.read()
                if ok:
                    frames.append(frame)
        else:
            # Some containers report an unreliable frame count; fall back
            # to reading everything and sampling from the buffer.
            buffer = []
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                buffer.append(frame)
            if buffer:
                frames = [buffer[i] for i in sample_frame_indices(len(buffer), num_frames)]
    finally:
        cap.release()

    if len(frames) < 2:
        raise ValueError(f"not enough frames could be read from video (got {len(frames)}, need >= 2): {video_path}")
    return frames


def normalize_frame_size(frames: list[np.ndarray]) -> list[np.ndarray]:
    """Resize every frame to the first frame's size."""
    target_h, target_w = frames[0].shape[:2]
    normalized = []
    for frame in frames:
        if frame.shape[:2] != (target_h, target_w):
            frame = cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_AREA)
        normalized.append(frame)
    return normalized


def build_depth_proxy(height: int, width: int, horizon_y: float) -> np.ndarray:
    """Return an (height, width) array: 0 at/above the horizon (far), 1 at the bottom row (near)."""
    if not 0.0 <= horizon_y <= 1.0:
        raise ValueError(f"horizon_y must be within [0, 1], got {horizon_y}")
    horizon_row = horizon_y * (height - 1)
    span = max((height - 1) - horizon_row, 1e-6)
    rows = np.arange(height, dtype=np.float32).reshape(height, 1)
    depth = np.clip((rows - horizon_row) / span, 0.0, 1.0)
    return np.repeat(depth, width, axis=1)


def resolve_direction(direction: str, seed: int) -> int:
    """Map a --direction value to a horizontal sign (+1 right, -1 left)."""
    if direction == "right":
        return 1
    if direction == "left":
        return -1
    if direction == "auto":
        # MVP simplification: no optical-flow direction estimate yet (that's
        # explicitly out of scope for this MVP). Pick deterministically from
        # the seed so "auto" still reproduces with --seed.
        return 1 if seed % 2 == 0 else -1
    raise ValueError(f"invalid direction: {direction!r} (expected one of {VALID_DIRECTIONS})")


def warp_frame_horizontal(frame: np.ndarray, x_shift: np.ndarray) -> np.ndarray:
    """Shift each pixel horizontally by `x_shift[row, col]` (in pixels)."""
    height, width = frame.shape[:2]
    x_coords, y_coords = np.meshgrid(np.arange(width, dtype=np.float32), np.arange(height, dtype=np.float32))
    map_x = (x_coords + x_shift).astype(np.float32)
    map_y = y_coords.astype(np.float32)
    return cv2.remap(frame, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def composite_motion_texture(
    frames: list[np.ndarray],
    horizon_y: float,
    strength: float,
    direction: str,
    seed: int,
) -> tuple[np.ndarray, int]:
    """Blend sampled frames into one image, streaking near rows more than far rows.

    Returns (image, resolved_direction) where resolved_direction is +1/-1.
    """
    if len(frames) < 2:
        raise ValueError("composite_motion_texture requires at least 2 frames")

    height, width = frames[0].shape[:2]
    depth = build_depth_proxy(height, width, horizon_y)
    alpha = (depth * BLEND_ALPHA_MAX)[:, :, None]
    resolved_direction = resolve_direction(direction, seed)
    rng = np.random.default_rng(seed)

    canvas = frames[0].astype(np.float32)
    num_frames = len(frames)
    for i in range(1, num_frames):
        t = i / (num_frames - 1)
        jitter = rng.uniform(0.85, 1.15)
        shift_amount = resolved_direction * strength * t * jitter
        x_shift = depth * shift_amount
        warped = warp_frame_horizontal(frames[i], x_shift).astype(np.float32)
        canvas = canvas * (1 - alpha) + warped * alpha

    return np.clip(canvas, 0, 255).astype(np.uint8), resolved_direction


def render_motion_texture(
    video_path: str | Path,
    output_dir: str | Path,
    frames: int = 12,
    horizon_y: float = 0.55,
    strength: float = 40.0,
    direction: str = "auto",
    seed: int = 0,
) -> tuple[Path, Path]:
    """Full pipeline: read, sample, composite, and save PNG + metadata JSON.

    Returns (image_path, metadata_path).
    """
    if direction not in VALID_DIRECTIONS:
        raise ValueError(f"invalid direction: {direction!r} (expected one of {VALID_DIRECTIONS})")

    raw_frames = read_video_frames(video_path, frames)
    normalized = normalize_frame_size(raw_frames)
    image, resolved_direction = composite_motion_texture(normalized, horizon_y, strength, direction, seed)

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(video_path).stem
    image_path = out_dir / f"{stem}_motion_texture.png"
    metadata_path = out_dir / f"{stem}_motion_texture.json"

    if not cv2.imwrite(str(image_path), image):
        raise IOError(f"failed to write output image: {image_path}")

    metadata = {
        "video": str(video_path),
        "frames_requested": frames,
        "frames_used": len(normalized),
        "horizon_y": horizon_y,
        "strength": strength,
        "direction": direction,
        "resolved_direction": "right" if resolved_direction == 1 else "left",
        "seed": seed,
        "output_width": int(image.shape[1]),
        "output_height": int(image.shape[0]),
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))

    return image_path, metadata_path
