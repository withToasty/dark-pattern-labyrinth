#!/usr/bin/env python3
"""Render a Motion Texture MVP image from a short video.

    python experiments/visual/motion_texture/render.py \\
      --video path/to/input.mp4 \\
      --output-dir experiments/visual/motion_texture/output/

Produces, in --output-dir:
  <name>_motion_texture.png    the composited motion texture image
  <name>_motion_texture.json   parameters used to produce it
"""

from __future__ import annotations

import argparse
import sys

from motion_texture import VALID_DIRECTIONS, render_motion_texture


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--video", required=True, help="path to the input video (mp4/mov)")
    parser.add_argument("--output-dir", required=True, help="directory for the PNG + metadata JSON")
    parser.add_argument("--frames", type=int, default=12, help="number of sampled frames (default: 12)")
    parser.add_argument(
        "--horizon-y",
        type=float,
        default=0.55,
        help="normalized horizon row, 0 (top) - 1 (bottom) (default: 0.55)",
    )
    parser.add_argument("--strength", type=float, default=40.0, help="near-field displacement in pixels (default: 40.0)")
    parser.add_argument("--direction", choices=VALID_DIRECTIONS, default="auto", help="streak direction (default: auto)")
    parser.add_argument("--seed", type=int, default=0, help="random seed for reproducibility (default: 0)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        image_path, metadata_path = render_motion_texture(
            video_path=args.video,
            output_dir=args.output_dir,
            frames=args.frames,
            horizon_y=args.horizon_y,
            strength=args.strength,
            direction=args.direction,
            seed=args.seed,
        )
    except (ValueError, FileNotFoundError, IOError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"wrote {image_path}")
    print(f"wrote {metadata_path}")


if __name__ == "__main__":
    main()
