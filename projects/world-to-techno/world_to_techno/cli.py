from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import build_arrangement, load_json


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Translate detected visual elements into a techno arrangement plan."
    )
    parser.add_argument("detections", help="Path to detections JSON")
    parser.add_argument(
        "--map",
        dest="sound_map",
        default="config/sound_map.json",
        help="Path to sound mapping JSON",
    )
    parser.add_argument(
        "--output",
        default="arrangement.json",
        help="Output arrangement JSON path",
    )
    args = parser.parse_args()

    detections = load_json(args.detections)
    sound_map = load_json(args.sound_map)

    arrangement = build_arrangement(detections, sound_map)

    output_path = Path(args.output)
    output_path.write_text(
        json.dumps(arrangement, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {output_path}")
    print(json.dumps(arrangement, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
