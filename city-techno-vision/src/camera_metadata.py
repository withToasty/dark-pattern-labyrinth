"""Read lightweight camera/lens metadata from image EXIF.

This module deliberately does not pretend that EXIF contains lens-distortion
calibration coefficients. It only extracts camera/lens hints that can be used
to choose whether a generic wide-angle approximation is appropriate.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from PIL import Image

TAG_MAKE = 271
TAG_MODEL = 272
TAG_ORIENTATION = 274
TAG_EXIF_IFD = 34665
TAG_FOCAL_LENGTH = 37386
TAG_FOCAL_LENGTH_35MM = 41989
TAG_LENS_MODEL = 42036

ULTRAWIDE_MAX_35MM_EQ = 18.0


@dataclass
class CameraMetadata:
    make: str | None = None
    model: str | None = None
    lens_model: str | None = None
    focal_length_mm: float | None = None
    focal_length_35mm: float | None = None
    orientation: int | None = None
    lens_mode: str = "unknown"

    def to_dict(self) -> dict:
        return asdict(self)


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError, ZeroDivisionError):
        pass
    numerator = getattr(value, "numerator", None)
    denominator = getattr(value, "denominator", None)
    if numerator is not None and denominator:
        return float(numerator) / float(denominator)
    return None


def _tag(exif, exif_ifd: dict, tag_id: int):
    value = exif.get(tag_id)
    if value is not None:
        return value
    return exif_ifd.get(tag_id)


def infer_lens_mode(
    lens_model: str | None,
    focal_length_35mm: float | None,
) -> str:
    label = (lens_model or "").casefold().replace("-", " ")
    if "ultra wide" in label or "ultrawide" in label:
        return "ultrawide"
    if focal_length_35mm is not None:
        if focal_length_35mm <= ULTRAWIDE_MAX_35MM_EQ:
            return "ultrawide"
        return "standard"
    return "unknown"


def read_camera_metadata(image_path: str | Path) -> CameraMetadata:
    """Return camera/lens hints without requiring them to be present.

    Messaging apps, web uploads, and image conversions often strip most EXIF.
    In that case fields remain None and lens_mode is "unknown".
    """
    try:
        with Image.open(image_path) as image:
            exif = image.getexif()
            exif_ifd = {}
            try:
                exif_ifd = exif.get_ifd(TAG_EXIF_IFD)
            except (AttributeError, KeyError, TypeError, ValueError):
                pass

            make = _tag(exif, exif_ifd, TAG_MAKE)
            model = _tag(exif, exif_ifd, TAG_MODEL)
            lens_model = _tag(exif, exif_ifd, TAG_LENS_MODEL)
            focal_length_mm = _as_float(_tag(exif, exif_ifd, TAG_FOCAL_LENGTH))
            focal_length_35mm = _as_float(_tag(exif, exif_ifd, TAG_FOCAL_LENGTH_35MM))
            orientation = _tag(exif, exif_ifd, TAG_ORIENTATION)
    except (OSError, ValueError):
        return CameraMetadata()

    lens_model_text = str(lens_model) if lens_model else None
    return CameraMetadata(
        make=str(make) if make else None,
        model=str(model) if model else None,
        lens_model=lens_model_text,
        focal_length_mm=focal_length_mm,
        focal_length_35mm=focal_length_35mm,
        orientation=int(orientation) if orientation is not None else None,
        lens_mode=infer_lens_mode(lens_model_text, focal_length_35mm),
    )
