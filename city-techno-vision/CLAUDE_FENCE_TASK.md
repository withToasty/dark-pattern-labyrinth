# Claude Task — Add Fence Recognition to city-techno-vision

## Goal

Extend the existing `city-techno-vision/` pipeline so that street-scene images can also return `fence` detections, while keeping the current Open Images V7 detector and the existing JSON/YAML contract intact.

This is an incremental extension, not a redesign.

---

## Current state — treat this as ground truth

The repository already has a working image-recognition project at:

`city-techno-vision/`

Relevant files:

- `city-techno-vision/detect.py`
- `city-techno-vision/src/detector.py`
- `city-techno-vision/src/visualize.py`
- `city-techno-vision/src/export.py`
- `city-techno-vision/README.md`

Current default model:

`yolov8n-oiv7.pt`

It already outputs:

- annotated image
- `detections.json`
- `detections.yaml`

Current detection schema:

```json
{
  "id": 1,
  "label": "car",
  "confidence": 0.94,
  "minx": 210,
  "maxx": 540,
  "miny": 620,
  "maxy": 850
}
```

The existing general detector works and must remain the primary detector.

YOLO-World support already exists, including `fence` in `DEFAULT_CITY_CLASSES`, but its actual fence quality has not been verified because the Claude sandbox blocked the one-time CLIP download. Do not make YOLO-World the primary solution for this task.

---

## Required design

Use two recognition paths on the same source image:

```text
image
├─ existing ObjectDetector
│  └─ Open Images V7 / normal street objects
│
└─ FenceDetector
   └─ semantic segmentation focused on fence
       ↓
       binary mask
       ↓
       connected components / region extraction
       ↓
       bbox conversion
       ↓
       Detection(label="fence", ...)
```

Merge both result lists before export.

After merging, reassign IDs sequentially so there are no collisions.

The final public JSON/YAML format must remain unchanged.

A fence result must look like:

```json
{
  "id": 8,
  "label": "fence",
  "confidence": 0.87,
  "minx": 34,
  "maxx": 1260,
  "miny": 390,
  "maxy": 810
}
```

Keep a segmentation mask as an optional debug artifact, but do not require downstream consumers to understand masks.

---

## Fence model direction

Prefer semantic segmentation over bounding-box training.

First target only:

`fence`

Do not split into school_fence / mesh_fence / guardrail / railing yet.

For training data, prefer an existing open/public dataset that already contains semantic `fence` labels, such as BDD100K.

Convert the source segmentation labels into a binary mask:

```text
fence = 1
everything else = 0
```

If a suitable publicly usable pretrained semantic-segmentation checkpoint with a fence class can be used with the existing Python stack, prefer that for the first working test.

If no suitable checkpoint is readily available, implement the smallest clean training/inference path needed for a fence-only model, but follow the resource limits below.

---

## Resource and token discipline — important

The user wants Claude token usage kept low.

Follow these rules strictly:

1. Do NOT perform a repo-wide review.
2. Do NOT recursively read unrelated folders.
3. Read only the five `city-techno-vision` files listed above first.
4. Only inspect another file when it is directly required by an import, test, or dependency.
5. Do NOT inspect or modify `Tk-work`.
6. Do NOT inspect or modify `projects/world-to-techno/` for this task.
7. Do NOT re-explain the repository architecture in long prose.
8. Do NOT generate a long design document before coding.
9. Reuse the existing `Detection`, export, visualization, and CLI structure wherever possible.
10. Prefer small edits over new abstractions.
11. Do not duplicate code that already exists.
12. Do not repeatedly rerun the same test after it has passed.
13. Do not search the web broadly. Only look up one specific dependency/model/dataset fact when it is necessary to proceed.
14. Do not download the full BDD100K dataset just to prove the integration.
15. Do not start a long full-dataset training run inside the Claude environment.
16. For integration tests, use a tiny sample, fixture, synthetic mask, or already-available image whenever possible.
17. Do not download multiple large candidate models. Choose one path, test it, and stop if blocked.
18. If an external download is blocked, report the exact domain/file needed and continue implementing everything that can be verified offline.
19. Keep final reporting short: changed files, what works, what remains blocked, exact next command.
20. Do not spend tokens proposing multiple architectures after a viable minimal path has been identified.

---

## Implementation preference

Aim for minimal changes similar to:

```text
city-techno-vision/
  detect.py
  src/
    detector.py
    fence_detector.py
    visualize.py
    export.py
```

Possible additional files are acceptable only when genuinely needed, e.g.:

```text
  scripts/
    prepare_fence_dataset.py
  tests/
    test_fence_detector.py
```

Do not create a new top-level project for fence recognition.

---

## Detection / mask conversion requirements

The FenceDetector should expose a small interface compatible with the current pipeline.

Conceptually:

```python
fence_detections = fence_detector.detect(image)
```

Return existing `Detection` objects if practical.

For mask → detection conversion:

- threshold the fence probability mask
- remove very small noisy regions
- extract connected regions
- calculate `minx, maxx, miny, maxy`
- calculate a reasonable confidence value from the fence probabilities inside the region
- emit `Detection(label="fence", ...)`

Do not overengineer post-processing in v1.

---

## CLI behavior

Existing usage must keep working:

```bash
python detect.py --image path/to/photo.jpg --output-dir output/
```

Add the fence path in a way that does not break the current command.

If a dedicated model weight is required, prefer a clear optional argument such as:

```bash
--fence-model path/to/fence_model.pt
```

If the fence model is unavailable, fail clearly or allow an explicit general-detector-only mode. Do not silently pretend fence detection ran.

---

## Output

Keep:

- annotated image
- `detections.json`
- `detections.yaml`

Optionally add:

- `fence_mask.png`

The existing JSON/YAML schema is the interface contract. Do not introduce a new top-level schema just for fence.

---

## Do not do

- Do not touch `Tk-work`.
- Do not modify `projects/world-to-techno/`.
- Do not implement audio generation.
- Do not implement BPM, MIDI, sound mapping, or music logic.
- Do not replace the existing Open Images V7 detector.
- Do not make YOLO-World the primary path.
- Do not use PLATEAU.
- Do not add Grounding DINO or SAM unless there is a hard, demonstrated reason and the user explicitly approves it.
- Do not manually collect or annotate hundreds of images.
- Do not redesign the existing export format.
- Do not split fence into multiple semantic subtypes yet.
- Do not start video/tracking work.

---

## Definition of done

The target is:

1. Existing Open Images V7 detections still work.
2. Fence recognition is an independent additional path.
3. A fence result is converted into the existing `Detection` format.
4. General objects + fence results are merged.
5. IDs are unique and sequential after merge.
6. Existing JSON/YAML output format is unchanged.
7. Existing annotated-image output still works.
8. A test or tiny end-to-end example demonstrates the merge path.
9. If actual fence-model weights cannot be obtained in the sandbox, the integration and model-loading path are still implemented and verified as far as possible, and the exact missing external artifact is reported.

---

## Work style

Start by reading only:

1. `city-techno-vision/detect.py`
2. `city-techno-vision/src/detector.py`
3. `city-techno-vision/src/visualize.py`
4. `city-techno-vision/src/export.py`
5. `city-techno-vision/README.md`

Then implement the smallest viable change.

Do not send a long preamble. Do not ask the user to repeat repository context already written in this file.

At the end, report only:

```text
Changed:
- ...

Verified:
- ...

Blocked:
- ...   # omit if none

Next command:
...
```
