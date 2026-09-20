"""Export detection results as JSON and YAML."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import yaml

from .detector import Detection


def build_result(filename: str, width: int, height: int, detections: list[Detection]) -> dict:
    return {
        "image": {
            "filename": filename,
            "width": width,
            "height": height,
        },
        "detections": [asdict(d) for d in detections],
    }


def write_json(result: dict, path: Path) -> None:
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_yaml(result: dict, path: Path) -> None:
    path.write_text(
        yaml.safe_dump(result, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
