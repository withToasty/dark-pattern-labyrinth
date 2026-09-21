"""Geometric horizon estimation from perspective line segments.

The estimator is model-free. It prefers an urban-scene method that needs only
one horizontal vanishing point:

1. detect long line segments,
2. estimate camera roll from a vertical vanishing point when possible,
3. find one dominant horizontal vanishing point,
4. draw the horizon through that point with the roll-derived orientation.

If that is not available, it falls back to the older two-horizontal-vanishing-
point method. Large images are internally downscaled for speed and results are
mapped back to the original image coordinates.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import cv2
import numpy as np

MAX_ANALYSIS_DIM = 1000
MAX_VP_LINES = 120

# Number of x,y samples used to describe the wide-angle distorted curve.
NUM_DISTORTED_POINTS = 7
# Generic ultra-wide bulge size used only when explicitly selected or inferred from metadata.
GENERIC_ULTRAWIDE_CURVE_STRENGTH = 0.015


@dataclass(frozen=True)
class DistortionSpec:
    """How the curved image-space horizon was obtained.

    This is intentionally explicit so an approximation can never be mistaken
    for measured lens calibration.
    """

    source: str
    model: str = "parabolic_approximation"
    curve_strength: float = GENERIC_ULTRAWIDE_CURVE_STRENGTH
    is_approximation: bool = True
    basis: str | None = None


def generic_ultrawide_distortion(source: str, basis: str | None = None) -> DistortionSpec:
    return DistortionSpec(source=source, basis=basis)


@dataclass
class VanishingPoint:
    x: float
    y: float
    supporting_lines: int


@dataclass
class HorizonResult:
    detected: bool
    method: str = "none"
    confidence: float = 0.0
    left_y: float | None = None
    right_y: float | None = None
    center_y: float | None = None
    center_y_normalized: float | None = None
    slope: float | None = None
    angle_deg: float | None = None
    supporting_lines: int = 0
    vanishing_points: list[VanishingPoint] | None = None
    width: float | None = None
    height: float | None = None
    distortion: DistortionSpec | None = None
    orientation_source: str | None = None
    vertical_vanishing_point: VanishingPoint | None = None

    def rectified_dict(self) -> dict | None:
        """Geometric straight-line horizon (the original single-layer output)."""
        if not self.detected or self.left_y is None or self.right_y is None or self.center_y is None:
            return None
        return {
            "type": "line",
            "center_y": round(float(self.center_y), 4),
            "center_y_normalized": (
                round(float(self.center_y_normalized), 4)
                if self.center_y_normalized is not None
                else None
            ),
            "left_y": round(float(self.left_y), 4),
            "right_y": round(float(self.right_y), 4),
            "slope": round(float(self.slope), 4) if self.slope is not None else None,
            "angle_deg": round(float(self.angle_deg), 4) if self.angle_deg is not None else None,
        }

    def distorted_dict(self) -> dict | None:
        """Image-space curved horizon, only when a distortion source is known.

        A generic parabola is allowed as an explicitly labelled approximation,
        but no curve is emitted when there is no metadata/manual lens hint.
        """
        if not self.detected or self.left_y is None or self.right_y is None or self.center_y is None:
            return None
        if self.width is None or self.height is None or self.distortion is None:
            return None
        points = _parabolic_distortion(
            self.left_y,
            self.right_y,
            self.center_y,
            self.width,
            self.height,
            self.distortion.curve_strength,
        )
        return {
            "type": "curve",
            "sampling": "polyline",
            "points": [[round(float(x), 4), round(float(y), 4)] for x, y in points],
            "curve_strength": round(float(self.distortion.curve_strength), 6),
            "distortion_source": self.distortion.source,
            "distortion_model": self.distortion.model,
            "is_approximation": self.distortion.is_approximation,
            "basis": self.distortion.basis,
            "center_y": round(float(self.center_y), 4),
            "center_y_normalized": (
                round(float(self.center_y_normalized), 4)
                if self.center_y_normalized is not None
                else None
            ),
        }

    def to_dict(self) -> dict:
        data = {
            "detected": self.detected,
            "method": self.method,
            "confidence": round(float(self.confidence), 4),
            "supporting_lines": self.supporting_lines,
            "orientation_source": self.orientation_source,
            "vanishing_points": None,
            "vertical_vanishing_point": None,
            "rectified": self.rectified_dict(),
            "distorted": self.distorted_dict(),
        }
        if self.vertical_vanishing_point is not None:
            point = self.vertical_vanishing_point
            data["vertical_vanishing_point"] = {
                "x": round(float(point.x), 2),
                "y": round(float(point.y), 2),
                "supporting_lines": point.supporting_lines,
            }
        if self.vanishing_points:
            data["vanishing_points"] = [
                {
                    "x": round(float(point.x), 2),
                    "y": round(float(point.y), 2),
                    "supporting_lines": point.supporting_lines,
                }
                for point in self.vanishing_points
            ]
        return data


def _parabolic_distortion(
    left_y: float,
    right_y: float,
    center_y: float,
    width: float,
    height: float,
    curve_strength: float,
    num_points: int = NUM_DISTORTED_POINTS,
) -> list[tuple[float, float]]:
    """Approximate a wide-angle horizon curve from the rectified straight line.

    Simple parabolic stand-in for barrel distortion: the curve matches the
    rectified line exactly at the image's horizontal center (distortion is
    weakest near the principal point) and bows away from the image's
    vertical center by an increasing amount toward the left/right edges,
    where lens distortion is strongest.
    """
    away_from_center = 1.0 if center_y >= height / 2 else -1.0
    max_offset = away_from_center * curve_strength * height
    span = max(width - 1, 1.0)

    points: list[tuple[float, float]] = []
    for index in range(num_points):
        x = span * index / (num_points - 1)
        base_y = left_y + (right_y - left_y) * (x / span)
        normalized_x = 2 * x / span - 1
        offset = max_offset * normalized_x**2
        points.append((x, base_y + offset))
    return points


def _line_angle(segment: tuple[float, float, float, float]) -> float:
    x1, y1, x2, y2 = segment
    angle = math.atan2(y2 - y1, x2 - x1)
    while angle >= math.pi / 2:
        angle -= math.pi
    while angle < -math.pi / 2:
        angle += math.pi
    return angle


def _line_length(segment: tuple[float, float, float, float]) -> float:
    x1, y1, x2, y2 = segment
    return math.hypot(x2 - x1, y2 - y1)


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


def _weighted_median(values_and_weights: list[tuple[float, float]]) -> float:
    ordered = sorted(values_and_weights, key=lambda item: item[0])
    total = sum(weight for _, weight in ordered)
    halfway = total / 2
    running = 0.0
    for value, weight in ordered:
        running += weight
        if running >= halfway:
            return value
    return ordered[-1][0]


def _best_vanishing_point(
    lines: list[tuple[float, float, float, float]],
    width: int,
    height: int,
    excluded: np.ndarray | None = None,
    inlier_angle_deg: float = 3.0,
    min_pair_angle_deg: float = 5.0,
) -> tuple[
    np.ndarray | None,
    np.ndarray | None,
    float,
    list[tuple[float, float, float, float]],
    np.ndarray,
]:
    if len(lines) < 3:
        return None, None, 0.0, [], np.array([], dtype=float)

    lengths = np.array([_line_length(line) for line in lines], dtype=float)

    if len(lines) > MAX_VP_LINES:
        selected_indices = np.argsort(-lengths)[:MAX_VP_LINES]
        selected_lines = [lines[index] for index in selected_indices]
        selected_lengths = lengths[selected_indices]
        selected_excluded = excluded[selected_indices] if excluded is not None else None
    else:
        selected_lines = lines
        selected_lengths = lengths
        selected_excluded = excluded

    center_x, center_y = width / 2, height / 2
    max_distance = 20 * max(width, height)
    threshold = math.radians(inlier_angle_deg)

    best_point = None
    best_inliers = None
    best_score = 0.0

    for i in range(len(selected_lines)):
        if selected_excluded is not None and selected_excluded[i]:
            continue
        for j in range(i + 1, len(selected_lines)):
            if selected_excluded is not None and selected_excluded[j]:
                continue

            angle_delta = abs(_line_angle(selected_lines[i]) - _line_angle(selected_lines[j]))
            angle_delta = min(angle_delta, math.pi - angle_delta)
            if math.degrees(angle_delta) < min_pair_angle_deg:
                continue

            point = _intersection(selected_lines[i], selected_lines[j])
            if point is None or not np.all(np.isfinite(point)):
                continue
            if math.hypot(point[0] - center_x, point[1] - center_y) > max_distance:
                continue

            errors = np.array([_angle_error(line, point) for line in selected_lines])
            inliers = errors < threshold
            if selected_excluded is not None:
                inliers &= ~selected_excluded

            score = float(selected_lengths[inliers].sum())
            if score > best_score:
                best_score = score
                best_point = point
                best_inliers = inliers

    return best_point, best_inliers, best_score, selected_lines, selected_lengths


def _extract_segments(image: np.ndarray) -> list[tuple[float, float, float, float]]:
    height, width = image.shape[:2]
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
        return []

    segments: list[tuple[float, float, float, float]] = []
    minimum_length = 0.06 * diagonal
    # OpenCV 4 commonly returns (N, 1, 4), while newer builds may return (N, 4).
    # Reshape both forms into a stable list of x1,y1,x2,y2 rows.
    for raw in np.asarray(raw_lines).reshape(-1, 4):
        line = tuple(float(value) for value in raw)
        if _line_length(line) >= minimum_length:
            segments.append(line)
    return segments


def _vertical_guided_horizon(
    segments: list[tuple[float, float, float, float]],
    width: int,
    height: int,
) -> HorizonResult:
    vertical_lines: list[tuple[float, float, float, float]] = []
    horizontal_candidates: list[tuple[float, float, float, float]] = []

    for line in segments:
        angle_deg = math.degrees(_line_angle(line))
        if abs(abs(angle_deg) - 90) <= 20:
            vertical_lines.append(line)
        if abs(angle_deg) <= 72:
            horizontal_candidates.append(line)

    if len(vertical_lines) < 6 or len(horizontal_candidates) < 6:
        return HorizonResult(detected=False)

    # One horizontal vanishing point fixes a point on the horizon.
    horizontal_point, horizontal_inliers, _, _, horizontal_lengths = _best_vanishing_point(
        horizontal_candidates, width, height
    )
    if (
        horizontal_point is None
        or horizontal_inliers is None
        or int(horizontal_inliers.sum()) < 4
    ):
        return HorizonResult(detected=False)

    # Prefer a vertical vanishing point over averaging apparent vertical-line
    # angles. This matters for ultra-wide photos: edge buildings can lean due
    # to perspective/lens distortion even when the phone itself is level.
    principal_x = (width - 1) / 2
    principal_y = (height - 1) / 2
    vertical_point, vertical_inliers, _, _, vertical_lengths = _best_vanishing_point(
        vertical_lines,
        width,
        height,
        inlier_angle_deg=3.0,
        min_pair_angle_deg=0.5,
    )

    vertical_vp = None
    orientation_source = "dominant_vertical_orientation"
    orientation_support = 0.0
    orientation_count = len(vertical_lines)

    stable_vertical_vp = False
    if vertical_point is not None and vertical_inliers is not None:
        vp_count = int(vertical_inliers.sum())
        vp_distance = math.hypot(
            float(vertical_point[0]) - principal_x,
            float(vertical_point[1]) - principal_y,
        )
        # A near-image intersection is often a facade/tower family rather than
        # the world-vertical vanishing point. Near-level phone shots normally
        # place the vertical VP well outside the frame.
        stable_vertical_vp = (
            vp_count >= 4
            and vp_distance >= min(width, height)
            and abs(float(vertical_point[1]) - principal_y) >= 0.5 * height
        )

    if stable_vertical_vp:
        dx = float(vertical_point[0]) - principal_x
        dy = float(vertical_point[1]) - principal_y
        slope = -dx / dy
        orientation_source = "vertical_vanishing_point"
        orientation_count = int(vertical_inliers.sum())
        orientation_support = float(
            vertical_lengths[vertical_inliers].sum()
            / max(vertical_lengths.sum(), 1.0)
        )
        vertical_vp = VanishingPoint(
            float(vertical_point[0]),
            float(vertical_point[1]),
            orientation_count,
        )
    else:
        # Fallback for parallel/synthetic verticals, where the vertical VP is
        # effectively at infinity.
        roll_samples: list[tuple[float, float]] = []
        for line in vertical_lines:
            angle_deg = math.degrees(_line_angle(line))
            if angle_deg < 0:
                angle_deg += 180
            deviation_from_vertical = angle_deg - 90
            roll_samples.append((deviation_from_vertical, _line_length(line)))

        roll_deg = _weighted_median(roll_samples)
        slope = math.tan(math.radians(roll_deg))
        total_vertical_weight = sum(weight for _, weight in roll_samples)
        concentrated_vertical_weight = sum(
            weight
            for deviation, weight in roll_samples
            if abs(deviation - roll_deg) <= 2.5
        )
        orientation_support = (
            concentrated_vertical_weight / total_vertical_weight
            if total_vertical_weight
            else 0.0
        )

    left_y = float(horizontal_point[1] + slope * (0 - horizontal_point[0]))
    right_y = float(
        horizontal_point[1] + slope * ((width - 1) - horizontal_point[0])
    )
    center_y = float(
        horizontal_point[1]
        + slope * ((width - 1) / 2 - horizontal_point[0])
    )

    if not (-0.25 * height <= center_y <= 1.25 * height):
        return HorizonResult(detected=False)

    horizontal_support = float(
        horizontal_lengths[horizontal_inliers].sum()
        / max(horizontal_lengths.sum(), 1.0)
    )
    horizontal_count_factor = min(1.0, int(horizontal_inliers.sum()) / 10.0)
    vertical_count_factor = min(1.0, orientation_count / 10.0)
    confidence = (
        0.40 * horizontal_support
        + 0.30 * orientation_support
        + 0.15 * horizontal_count_factor
        + 0.15 * vertical_count_factor
    )
    confidence = max(0.0, min(1.0, confidence))

    return HorizonResult(
        detected=True,
        method="vertical_guided_single_vp",
        confidence=confidence,
        left_y=left_y,
        right_y=right_y,
        center_y=center_y,
        center_y_normalized=center_y / height,
        slope=slope,
        angle_deg=math.degrees(math.atan(slope)),
        supporting_lines=int(horizontal_inliers.sum()) + orientation_count,
        vanishing_points=[
            VanishingPoint(
                float(horizontal_point[0]),
                float(horizontal_point[1]),
                int(horizontal_inliers.sum()),
            )
        ],
        orientation_source=orientation_source,
        vertical_vanishing_point=vertical_vp,
    )

def _two_vanishing_point_horizon(
    segments: list[tuple[float, float, float, float]],
    width: int,
    height: int,
) -> HorizonResult:
    lines = [line for line in segments if abs(math.degrees(_line_angle(line))) <= 72]
    if len(lines) < 6:
        return HorizonResult(detected=False, supporting_lines=len(lines))

    first_point, first_inliers, _, selected_lines, selected_lengths = _best_vanishing_point(
        lines, width, height
    )
    if first_point is None or first_inliers is None or int(first_inliers.sum()) < 3:
        return HorizonResult(detected=False, supporting_lines=len(lines))

    second_point, second_inliers, _, _, _ = _best_vanishing_point(
        selected_lines, width, height, excluded=first_inliers
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

    support_mask = first_inliers | second_inliers
    coverage = float(selected_lengths[support_mask].sum() / max(selected_lengths.sum(), 1.0))
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
        method="two_horizontal_vanishing_points",
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


def _rescale_result(
    result: HorizonResult, scale: float, original_width: int, original_height: int
) -> HorizonResult:
    if not result.detected:
        return result

    if scale != 1.0:
        for attribute in ("left_y", "right_y", "center_y"):
            value = getattr(result, attribute)
            if value is not None:
                setattr(result, attribute, value / scale)

        if result.vanishing_points:
            for point in result.vanishing_points:
                point.x /= scale
                point.y /= scale
        if result.vertical_vanishing_point is not None:
            result.vertical_vanishing_point.x /= scale
            result.vertical_vanishing_point.y /= scale

    if result.center_y is not None:
        result.center_y_normalized = result.center_y / original_height

    result.width = original_width
    result.height = original_height
    return result


def estimate_horizon(
    image: np.ndarray,
    distortion: DistortionSpec | None = None,
) -> HorizonResult:
    """Estimate the geometric horizon in original-image pixel coordinates."""
    if image is None or image.ndim < 2:
        return HorizonResult(detected=False)

    original_height, original_width = image.shape[:2]
    if original_width < 80 or original_height < 80:
        return HorizonResult(detected=False)

    scale = min(1.0, MAX_ANALYSIS_DIM / max(original_width, original_height))
    if scale < 1.0:
        working = cv2.resize(
            image,
            (round(original_width * scale), round(original_height * scale)),
            interpolation=cv2.INTER_AREA,
        )
    else:
        working = image

    height, width = working.shape[:2]
    segments = _extract_segments(working)
    if len(segments) < 6:
        return HorizonResult(detected=False, supporting_lines=len(segments))

    result = _vertical_guided_horizon(segments, width, height)
    if not result.detected:
        result = _two_vanishing_point_horizon(segments, width, height)

    result = _rescale_result(result, scale, original_width, original_height)
    if result.detected:
        result.distortion = distortion
    return result
