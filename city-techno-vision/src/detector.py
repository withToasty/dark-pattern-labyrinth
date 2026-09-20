"""Object detection wrapper around an Ultralytics YOLO model.

Responsibility: image in, structured detections out. Nothing about
sound, rhythm, or MIDI belongs in this module (that's a separate
project layered on top of this one's JSON/YAML output).
"""

from __future__ import annotations

from dataclasses import dataclass

from ultralytics import YOLO


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

    def __init__(self, model_path: str = "yolov8n.pt", confidence_threshold: float = 0.25):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold

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
