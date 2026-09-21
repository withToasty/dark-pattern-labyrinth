from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_SCREEN_AREA = 0.10
DEFAULT_MOTION = 0.20


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def intensity_for(item: dict[str, Any]) -> float:
    confidence = clamp(float(item.get("confidence", 0.0)))
    screen_area = clamp(float(item.get("screen_area", DEFAULT_SCREEN_AREA)))
    motion = clamp(float(item.get("motion", DEFAULT_MOTION)))

    score = confidence * 0.55 + screen_area * 0.30 + motion * 0.15
    return round(clamp(score), 3)


def choose_bpm(layers: list[dict[str, Any]]) -> int:
    if not layers:
        return 128

    motion_values = [float(layer.get("motion", DEFAULT_MOTION)) for layer in layers]
    mean_motion = sum(motion_values) / len(motion_values)

    # 初期ルール。映像の動きが大きいほど少し速くする。
    return round(124 + clamp(mean_motion) * 16)


def build_arrangement(
    detections: list[dict[str, Any]],
    sound_map: dict[str, dict[str, str]],
) -> dict[str, Any]:
    layers: list[dict[str, Any]] = []
    unknown: list[str] = []

    for item in detections:
        label = str(item.get("label", "")).strip()
        if not label:
            continue

        mapping = sound_map.get(label)
        if mapping is None:
            unknown.append(label)
            continue

        layers.append(
            {
                "source": label,
                "role": mapping["role"],
                "pattern": mapping["pattern"],
                "intensity": intensity_for(item),
                "confidence": round(clamp(float(item.get("confidence", 0.0))), 3),
                "screen_area": round(
                    clamp(float(item.get("screen_area", DEFAULT_SCREEN_AREA))), 3
                ),
                "motion": round(clamp(float(item.get("motion", DEFAULT_MOTION))), 3),
            }
        )

    layers.sort(key=lambda x: x["intensity"], reverse=True)

    return {
        "bpm": choose_bpm(layers),
        "layer_count": len(layers),
        "layers": layers,
        "unknown_labels": sorted(set(unknown)),
    }


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))
