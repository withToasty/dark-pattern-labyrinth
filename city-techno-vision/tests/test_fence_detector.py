"""Offline tests for fence mask conversion, merge, and predict-mask plumbing."""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.detector import Detection, merge_detections
from src.fence_detector import CITYSCAPES_FENCE_CLASS_ID, FenceDetector, mask_to_detections


def _synthetic_fence_mask() -> np.ndarray:
    mask = np.zeros((100, 200), dtype=np.float32)
    mask[10:40, 20:150] = 0.9
    mask[80:83, 5:8] = 0.95
    return mask


def test_mask_to_detections_extracts_region_and_drops_noise():
    detections = mask_to_detections(_synthetic_fence_mask(), threshold=0.5, min_area=500)

    assert len(detections) == 1
    det = detections[0]
    assert det.label == "fence"
    assert det.id == 1
    assert (det.minx, det.miny, det.maxx, det.maxy) == (20, 10, 150, 40)
    assert 0.85 <= det.confidence <= 0.95


def test_merge_detections_reassigns_sequential_ids():
    general = [
        Detection(id=1, label="car", confidence=0.9, minx=0, maxx=10, miny=0, maxy=10),
        Detection(id=2, label="person", confidence=0.8, minx=5, maxx=15, miny=5, maxy=15),
    ]
    fence = mask_to_detections(_synthetic_fence_mask(), threshold=0.5, min_area=500)

    merged = merge_detections(general, fence)

    assert [d.id for d in merged] == [1, 2, 3]
    assert [d.label for d in merged] == ["car", "person", "fence"]
    assert general[0].id == 1 and general[1].id == 2
    assert fence[0].id == 1


def test_predict_mask_upsamples_and_selects_fence_class():
    torch = __import__("torch")

    height, width = 40, 60
    reduced_h, reduced_w = 4, 6
    num_labels = 19

    logits = torch.zeros(1, num_labels, reduced_h, reduced_w)
    logits[0, CITYSCAPES_FENCE_CLASS_ID, 0:2, 0:3] = 10.0

    class FakeOutput:
        def __init__(self, logits):
            self.logits = logits

    class FakeModel:
        def __call__(self, **inputs):
            assert "pixel_values" in inputs
            return FakeOutput(logits)

    class FakeProcessor:
        def __call__(self, images, return_tensors):
            assert return_tensors == "pt"
            return {"pixel_values": torch.zeros(1, 3, reduced_h, reduced_w)}

    detector = FenceDetector.__new__(FenceDetector)
    detector.model = FakeModel()
    detector.processor = FakeProcessor()
    detector.fence_class_id = CITYSCAPES_FENCE_CLASS_ID

    image = np.zeros((height, width, 3), dtype=np.uint8)
    mask = detector.predict_mask(image)

    assert mask.shape == (height, width)
    assert mask.dtype == np.float32
    assert mask[2, 2] > 0.8
    assert mask[height - 1, width - 1] < 0.2
