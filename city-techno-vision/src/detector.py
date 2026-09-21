"""Object detection wrapper around an Ultralytics YOLO model.

Responsibility: image in, structured detections out. Nothing about
sound, rhythm, or MIDI belongs in this module (that's a separate
project layered on top of this one's JSON/YAML output).

Two kinds of model are supported, selected by which weights you pass in:

- A regular YOLO model (e.g. "yolov8n.pt") only ever detects the 80
  everyday objects it was trained on (car, person, dog, ...). Its
  class list is fixed at training time.
- A YOLO-World model (e.g. "yolov8s-worldv2.pt") is open-vocabulary:
  you hand it any list of words at runtime (`classes=[...]`) and it
  looks for those instead.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

DEFAULT_CITY_CLASSES = [
    "car",
    "truck",
    "bus",
    "motorcycle",
    "bicycle",
    "person",
    "traffic light",
    "traffic sign",
    "building",
    "sky",
    "cloud",
    "tree",
    "fence",
    "road",
    "sidewalk",
    "streetlight",
    "bridge",
    "billboard",
    "utility pole",
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


class ObjectDetector:
    """Loads a YOLO model once and runs detection on individual images."""

    def __init__(
        self,
        model_path: str = "yolov8n-oiv7.pt",
        confidence_threshold: float = 0.15,
        classes: list[str] | None = None,
    ):
        from ultralytics import YOLO

        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold

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
