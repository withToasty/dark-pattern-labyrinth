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
  looks for those instead. That's how "building", "sky", "cloud",
  "fence" etc. become detectable without retraining anything -- it's
  just a list of words, not a new model. The only real cost is a
  one-time download of a CLIP text encoder the first time
  `set_classes` runs (see README: "open-vocabulary detection").
"""

from __future__ import annotations

from dataclasses import dataclass

from ultralytics import YOLO

# A reasonably broad default vocabulary for street/city scenes, used
# automatically when a YOLO-World model is loaded without an explicit
# --classes override. Edit this list freely -- with a world model,
# adding a word here costs nothing extra (no retraining, no new
# download) once the one-time CLIP text encoder is cached locally.
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
    """One detected object, in image pixel coordinates.

    Coordinate system: origin at the image's top-left corner,
    x increasing to the right, y increasing downward.
    """

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
        confidence_threshold: float = 0.25,
        classes: list[str] | None = None,
    ):
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
