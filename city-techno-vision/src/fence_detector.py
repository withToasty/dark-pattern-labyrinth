"""Fence recognition via semantic segmentation."""

from __future__ import annotations

import cv2
import numpy as np

from .detector import Detection

CITYSCAPES_FENCE_CLASS_ID = 4
DEFAULT_FENCE_MODEL_ID = "nvidia/segformer-b0-finetuned-cityscapes-1024-1024"


def mask_to_detections(
    mask: np.ndarray,
    threshold: float = 0.5,
    min_area: int = 500,
    label: str = "fence",
) -> list[Detection]:
    """Convert a per-pixel fence-probability mask into Detection boxes."""
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
            )
        )
    return detections


class FenceDetector:
    """Loads a SegFormer/Cityscapes checkpoint and runs fence detection."""

    def __init__(
        self,
        model_path: str = DEFAULT_FENCE_MODEL_ID,
        confidence_threshold: float = 0.5,
        min_area: int = 500,
        fence_class_id: int = CITYSCAPES_FENCE_CLASS_ID,
    ):
        self.confidence_threshold = confidence_threshold
        self.min_area = min_area
        self.fence_class_id = fence_class_id
        self.model, self.processor = self._load_model(model_path)

    @staticmethod
    def _load_model(model_path: str):
        try:
            from transformers import SegformerForSemanticSegmentation, SegformerImageProcessor
        except ImportError as exc:
            raise RuntimeError(
                "fence detection requires 'torch', 'transformers', 'pillow' and "
                "'torchvision'. Install them and pass --fence-model "
                "<huggingface-model-id-or-local-path> "
                f"(default: {DEFAULT_FENCE_MODEL_ID})."
            ) from exc
        try:
            processor = SegformerImageProcessor.from_pretrained(model_path)
            model = SegformerForSemanticSegmentation.from_pretrained(model_path)
        except OSError as exc:
            raise RuntimeError(
                f"could not load fence model '{model_path}': {exc}. If this is a "
                "network/proxy block on huggingface.co, download that model's files "
                "another way and pass a local directory path instead."
            ) from exc
        model.eval()
        return model, processor

    def predict_mask(self, image: np.ndarray) -> np.ndarray:
        """Run segmentation; return a fence-probability mask with the input H,W."""
        import torch

        height, width = image.shape[:2]
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        inputs = self.processor(images=rgb, return_tensors="pt")
        with torch.no_grad():
            logits = self.model(**inputs).logits
            upsampled = torch.nn.functional.interpolate(
                logits, size=(height, width), mode="bilinear", align_corners=False
            )
            probs = torch.softmax(upsampled, dim=1)
            fence_prob = probs[0, self.fence_class_id]
        return fence_prob.cpu().numpy().astype(np.float32)

    def detect(self, image: np.ndarray) -> list[Detection]:
        mask = self.predict_mask(image)
        return mask_to_detections(mask, threshold=self.confidence_threshold, min_area=self.min_area)
