"""Object detection wrappers for fixed- and open-vocabulary YOLO models.

Responsibility: image in, structured detections out. Nothing about sound,
rhythm, or MIDI belongs in this module.
"""

from __future__ import annotations

from dataclasses import dataclass, replace


DEFAULT_CONFIDENCE_THRESHOLD = 0.05
DEFAULT_WORLD_MODEL_ID = "yolov8s-worldv2.pt"

# Broad city-scene vocabulary for the supplemental YOLO-World pass.  The goal
# here is recall: downstream music mapping can decide which detections to use.
DEFAULT_CITY_CLASSES = [
    # vehicles / people
    "car",
    "taxi",
    "truck",
    "bus",
    "van",
    "motorcycle",
    "bicycle",
    "person",
    # roads / transport infrastructure
    "road",
    "sidewalk",
    "curb",
    "crosswalk",
    "lane marking",
    "guardrail",
    "road barrier",
    "railing",
    "bridge",
    "overpass",
    "tunnel",
    "railway",
    "train",
    "stairs",
    # street furniture / utilities
    "traffic light",
    "traffic sign",
    "streetlight",
    "utility pole",
    "power line",
    "bollard",
    "bench",
    "trash can",
    "vending machine",
    # buildings / facade details
    "building",
    "apartment building",
    "skyscraper",
    "house",
    "window",
    "door",
    "balcony",
    "roof",
    "awning",
    "shutter",
    "billboard",
    "shop sign",
    "air conditioner",
    "antenna",
    "chimney",
    # scene / nature
    "fence",
    "wall",
    "tree",
    "bush",
    "grass",
    "plant",
    "sky",
    "cloud",
    "mountain",
    "water",
    "puddle",
]


@dataclass
class Detection:
    """One detected object, in image pixel coordinates."""

    id: int
    label: str
    confidence: float
    minx: int
    maxx: int
    miny: int
    maxy: int
    source: str = "yolo"


class ObjectDetector:
    """Loads a YOLO model once and runs detection on individual images."""

    def __init__(
        self,
        model_path: str = "yolov8n-oiv7.pt",
        confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
        classes: list[str] | None = None,
        source: str = "yolo",
    ):
        from ultralytics import YOLO

        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self.source = source

        if classes:
            if not hasattr(self.model, "set_classes"):
                raise ValueError(
                    f"'{model_path}' is a fixed-class model and can't take --classes. "
                    "Use an open-vocabulary model such as yolov8s-worldv2.pt instead."
                )
            self.model.set_classes(classes)

    def detect(self, image_path: str) -> list[Detection]:
        results = self.model.predict(image_path, conf=self.confidence_threshold, verbose=False)
        result = results[0]
        class_names = result.names

        detections: list[Detection] = []
        for detection_id, box in enumerate(result.boxes, start=1):
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            detections.append(
                Detection(
                    id=detection_id,
                    label=class_names[class_id],
                    confidence=round(confidence, 4),
                    minx=round(x1),
                    maxx=round(x2),
                    miny=round(y1),
                    maxy=round(y2),
                    source=self.source,
                )
            )
        return detections


def merge_detections(*detection_lists: list[Detection]) -> list[Detection]:
    """Concatenate detection lists, reassigning ids sequentially so none collide."""
    merged: list[Detection] = []
    for detections in detection_lists:
        for det in detections:
            merged.append(replace(det, id=len(merged) + 1))
    return merged
