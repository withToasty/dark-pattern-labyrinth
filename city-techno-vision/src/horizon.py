"""Geometric horizon estimation from perspective line segments.

The estimator is intentionally model-free: it detects long non-vertical line
segments, finds two dominant horizontal vanishing points, and connects them.
It works best on man-made scenes (roads/buildings) and returns detected=False
when the geometry is too weak instead of inventing a horizon.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math

import cv2
import numpy as np


@dataclass
class VanishingPoint:
    x: float
    y: float
    supporting_lines: int


@dataclass
class HorizonResult:
    detected: bool
    method: str = "line_vanishing_points"
    confidence: float = 0.0
    left_y: float | None = None
    right_y: float | None = None
    center_y: float | None = None
    center_y_normalized: float | None = None
    slope: float | None = None
    angle_deg: float | None = None
    supporting_lines: int = 0
    vanishing_points: list[VanishingPoint] | None = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["confidence"] = round(float(self.confidence), 4)
        for key in ("left_y", "right_y", "center_y", "center_y_normalized", "slope", "angle_deg"):
            if data[key] is not None:
                data[key] = round(float(data[key]), 4)
        if data["vanishing_points"]:
            for point in data["vanishing_points"]:
                point["x"] = round(float(point["x"]), 2)
                point["y"] = round(float(point["y"]), 2)
        return data


def _line_angle(segment: tuple[float, float, float, float]) -> float:
    x1, y1, x2, y2 = segment
    angle = math.atan2(y2 - y1, x2 - x1)
    while angle >= math.pi / 2:
        angle -= math.pi
    while angle < -math.pi / 2:
        angle += math.pi
    return angle


def _intersection(
    first: tuple[float, float, float, float],
    second: tuple[float, float, float, float],
) -> np.ndarray | None:
    x1, y1, x2, y2 = first
    x3, y3, x4, y4 = second

    a1, b1 = y2 - y1, x1 - x2
    a2, b2 = y4 - y3, x3 - x4
    c1 = a1 * x1 + b1 * y1
    c2 = a2 * x3 + b2 * y3
    determinant = a1 * b2 - a2 * b1
    if abs(determinant) < 1e-8:
        return None

    return np.array(
        [
            (b2 * c1 - b1 * c2) / determinant,
            (a1 * c2 - a2 * c1) / determinant,
        ],
        dtype=float,
    )


def _angle_error(segment: tuple[float, float, float, float], point: np.ndarray) -> float:
    x1, y1, x2, y2 = segment
    midpoint_x = (x1 + x2) / 2
    midpoint_y = (y1 + y2) / 2

    line_x, line_y = x2 - x1, y2 - y1
    point_x, point_y = point[0] - midpoint_x, point[1] - midpoint_y
    line_norm = math.hypot(line_x, line_y)
    point_norm = math.hypot(point_x, point_y)
    if line_norm < 1e-6 or point_norm < 1e-6:
        return math.pi / 2

    cosine = abs((line_x * point_x + line_y * point_y) / (line_norm * point_norm))
    cosine = min(1.0, max(0.0, cosine))
    return math.acos(cosine)


def _best_vanishing_point(
    lines: list[tuple[float, float, float, float]],
    width: int,
    height: int,
    excluded: np.ndarray | None = None,
    inlier_angle_deg: float = 3.0,
) -> tuple[np.ndarray | None, np.ndarray | None, float]:
    if len(lines) < 3:
        return None, None, 0.0

    lengths = np.array(
        [math.hypot(line[2] - line[0], line[3] - line[1]) for line in lines],
        dtype=float,
    )
    center_x, center_y = width / 2, height / 2
    max_distance = 20 * max(width, height)
    threshold = math.radians(inlier_angle_deg)

    best_point = None
    best_inliers = None
    best_score = 0.0

    for i in range(len(lines)):
        if excluded is not None and excluded[i]:
            continue
        for j in range(i + 1, len(lines)):
            if excluded is not None and excluded[j]:
                continue

            angle_delta = abs(_line_angle(lines[i]) - _line_angle(lines[j]))
            angle_delta = min(angle_delta, math.pi - angle_delta)
            if math.degrees(angle_delta) < 6.0:
                continue

            point = _intersection(lines[i], lines[j])
            if point is None or not np.all(np.isfinite(point)):
                continue
            if math.hypot(point[0] - center_x, point[1] - center_y) > max_distance:
                continue

            errors = np.array([_angle_error(line, point) for line in lines])
            inliers = errors < threshold
            if excluded is not None:
                inliers &= ~excluded

            score = float(lengths[inliers].sum())
            if score > best_score:
                best_score = score
                best_point = point
                best_inliers = inliers

    return best_point, best_inliers, best_score


def estimate_horizon(image: np.ndarray) -> HorizonResult:
    """Estimate the geometric horizon in image coordinates."""
    if image is None or image.ndim < 2:
        return HorizonResult(detected=False)

    height, width = image.shape[:2]
    if width < 80 or height < 80:
        return HorizonResult(detected=False)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image.copy()
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray, 50, 150)

    diagonal = math.hypot(width, height)
    raw_lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=max(30, int(0.04 * min(width, height))),
        minLineLength=max(30, int(0.06 * diagonal)),
        maxLineGap=max(10, int(0.02 * diagonal)),
    )
    if raw_lines is None:
        return HorizonResult(detected=False)

    lines: list[tuple[float, float, float, float]] = []
    for raw in raw_lines[:, 0, :]:
        line = tuple(float(value) for value in raw)
        length = math.hypot(line[2] - line[0], line[3] - line[1])
        angle_deg = abs(math.degrees(_line_angle(line)))
        if length >= 0.06 * diagonal and angle_deg <= 72:
            lines.append(line)

    if len(lines) < 6:
        return HorizonResult(detected=False, supporting_lines=len(lines))

    first_point, first_inliers, _ = _best_vanishing_point(lines, width, height)
    if first_point is None or first_inliers is None or int(first_inliers.sum()) < 3:
        return HorizonResult(detected=False, supporting_lines=len(lines))

    second_point, second_inliers, _ = _best_vanishing_point(
        lines, width, height, excluded=first_inliers
    )
    if second_point is None or second_inliers is None or int(second_inliers.sum()) < 3:
        return HorizonResult(detected=False, supporting_lines=int(first_inliers.sum()))

    if abs(second_point[0] - first_point[0]) < 0.3 * width:
        return HorizonResult(
            detected=False,
            supporting_lines=int(first_inliers.sum() + second_inliers.sum()),
        )

    dx = float(second_point[0] - first_point[0])
    slope = float((second_point[1] - first_point[1]) / dx)
    left_y = float(first_point[1] + slope * (0 - first_point[0]))
    right_y = float(first_point[1] + slope * ((width - 1) - first_point[0]))
    center_y = float(first_point[1] + slope * ((width - 1) / 2 - first_point[0]))

    if not (-0.25 * height <= center_y <= 1.25 * height):
        return HorizonResult(
            detected=False,
            supporting_lines=int(first_inliers.sum() + second_inliers.sum()),
        )

    lengths = np.array(
        [math.hypot(line[2] - line[0], line[3] - line[1]) for line in lines],
        dtype=float,
    )
    support_mask = first_inliers | second_inliers
    coverage = float(lengths[support_mask].sum() / max(lengths.sum(), 1.0))
    first_count = int(first_inliers.sum())
    second_count = int(second_inliers.sum())
    balance = min(first_count, second_count) / max(first_count, second_count, 1)
    support_factor = min(1.0, min(first_count, second_count) / 5.0)
    confidence = max(0.0, min(1.0, coverage * (0.5 + 0.5 * balance) * support_factor))

    points = [
        VanishingPoint(float(first_point[0]), float(first_point[1]), first_count),
        VanishingPoint(float(second_point[0]), float(second_point[1]), second_count),
    ]
    points.sort(key=lambda point: point.x)

    return HorizonResult(
        detected=True,
        confidence=confidence,
        left_y=left_y,
        right_y=right_y,
        center_y=center_y,
        center_y_normalized=center_y / height,
        slope=slope,
        angle_deg=math.degrees(math.atan(slope)),
        supporting_lines=int(support_mask.sum()),
        vanishing_points=points,
    )
