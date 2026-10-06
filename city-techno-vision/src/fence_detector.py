"""Cityscapes semantic segmentation for fence and other static scene regions."""

from __future__ import annotations

import cv2
import numpy as np

from .detector import Detection, merge_detections

CITYSCAPES_CLASS_IDS = {
    "road": 0,
    "sidewalk": 1,
    "building": 2,
    "wall": 3,
    "fence": 4,
    "pole": 5,
    "traffic light": 6,
    "traffic sign": 7,
    "vegetation": 8,
    "terrain": 9,
    "sky": 10,
    "person": 11,
    "rider": 12,
    "car": 13,
    "truck": 14,
    "bus": 15,
    "train": 16,
    "motorcycle": 17,
    "bicycle": 18,
}

CITYSCAPES_FENCE_CLASS_ID = CITYSCAPES_CLASS_IDS["fence"]
DEFAULT_FENCE_MODEL_ID = "nvidia/segformer-b0-finetuned-cityscapes-1024-1024"
DEFAULT_SEGMENTATION_CLASSES = (
    "road",
    "sidewalk",
    "building",
    "wall",
    "fence",
    "pole",
    "vegetation",
    "terrain",
    "sky",
)
DEFAULT_SEGMENTATION_THRESHOLD = 0.35
DEFAULT_SEGMENTATION_MIN_AREA = 300


def mask_to_detections(
    mask: np.ndarray,
    threshold: float = DEFAULT_SEGMENTATION_THRESHOLD,
    min_area: int = DEFAULT_SEGMENTATION_MIN_AREA,
    label: str = "fence",
    source: str = "segformer",
) -> list[Detection]:
    """Convert one per-pixel class-probability mask into Detection boxes."""
    binary = (mask >= threshold).astype(np.uint8)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)

    detections: list[Detection] = []
    for component_id in range(1, num_labels):
        area = int(stats[component_id, cv2.CC_STAT_AREA])
        if area < min_area:
            continue
        x = int(stats[component_id, cv2.CC_STAT_LEFT])
        y = int(stats[component_id, cv2.CC_STAT_TOP])
        w = int(stats[component_id, cv2.CC_STAT_WIDTH])
        h = int(stats[component_id, cv2.CC_STAT_HEIGHT])
        region_probs = mask[labels == component_id]
        confidence = float(region_probs.mean()) if region_probs.size else 0.0
        detections.append(
            Detection(
                id=len(detections) + 1,
                label=label,
                confidence=round(confidence, 4),
                minx=x,
                maxx=x + w,
                miny=y,
                maxy=y + h,
                source=source,
            )
        )
    return detections


class CityscapesDetector:
    """Loads a SegFormer/Cityscapes checkpoint and extracts selected classes."""

    def __init__(
        self,
        model_path: str = DEFAULT_FENCE_MODEL_ID,
        confidence_threshold: float = DEFAULT_SEGMENTATION_THRESHOLD,
        min_area: int = DEFAULT_SEGMENTATION_MIN_AREA,
        class_names: tuple[str, ...] | list[str] | None = None,
    ):
        self.confidence_threshold = confidence_threshold
        self.min_area = min_area
        self.class_names = tuple(class_names or DEFAULT_SEGMENTATION_CLASSES)
        unknown = [name for name in self.class_names if name not in CITYSCAPES_CLASS_IDS]
        if unknown:
            raise ValueError(f"unknown Cityscapes classes: {', '.join(unknown)}")
        self.fence_class_id = CITYSCAPES_FENCE_CLASS_ID
        self.model, self.processor = self._load_model(model_path)

    @staticmethod
    def _load_model(model_path: str):
        try:
            from transformers import SegformerForSemanticSegmentation, SegformerImageProcessor
        except ImportError as exc:
            raise RuntimeError(
                "scene segmentation requires 'torch', 'transformers', 'pillow' and "
                "'torchvision'. Install them and pass --fence-model "
                "<huggingface-model-id-or-local-path> "
                f"(default: {DEFAULT_FENCE_MODEL_ID})."
            ) from exc
        try:
            processor = SegformerImageProcessor.from_pretrained(model_path)
            model = SegformerForSemanticSegmentation.from_pretrained(model_path)
        except OSError as exc:
            raise RuntimeError(
                f"could not load segmentation model '{model_path}': {exc}. If this is a "
                "network/proxy block on huggingface.co, download that model's files "
                "another way and pass a local directory path instead."
            ) from exc
        model.eval()
        return model, processor

    def _predict_probabilities(self, image: np.ndarray):
        import torch

        height, width = image.shape[:2]
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        inputs = self.processor(images=rgb, return_tensors="pt")
        with torch.no_grad():
            logits = self.model(**inputs).logits
            upsampled = torch.nn.functional.interpolate(
                logits, size=(height, width), mode="bilinear", align_corners=False
            )
            return torch.softmax(upsampled, dim=1)

    def predict_masks(
        self,
        image: np.ndarray,
        class_names: tuple[str, ...] | list[str] | None = None,
    ) -> dict[str, np.ndarray]:
        """Run segmentation once and return probability masks for selected classes."""
        names = tuple(class_names or self.class_names)
        unknown = [name for name in names if name not in CITYSCAPES_CLASS_IDS]
        if unknown:
            raise ValueError(f"unknown Cityscapes classes: {', '.join(unknown)}")
        probs = self._predict_probabilities(image)
        return {
            name: probs[0, CITYSCAPES_CLASS_IDS[name]].cpu().numpy().astype(np.float32)
            for name in names
        }

    def predict_mask(self, image: np.ndarray) -> np.ndarray:
        """Backward-compatible fence-only probability mask."""
        probs = self._predict_probabilities(image)
        return probs[0, self.fence_class_id].cpu().numpy().astype(np.float32)

    def detect(
        self,
        image: np.ndarray,
        class_names: tuple[str, ...] | list[str] | None = None,
    ) -> list[Detection]:
        masks = self.predict_masks(image, class_names=class_names)
        per_class = [
            mask_to_detections(
                mask,
                threshold=self.confidence_threshold,
                min_area=self.min_area,
                label=label,
            )
            for label, mask in masks.items()
        ]
        return merge_detections(*per_class)


# Compatibility with existing imports/tests and the --fence-model flag.
FenceDetector = CityscapesDetector
