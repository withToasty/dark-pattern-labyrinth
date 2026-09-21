"""FastAPI web app for city-techno-vision.

Browser -> POST /api/analyze (multipart image) -> existing detection/fence/
horizon pipeline (src/pipeline.py, shared with detect.py's CLI) -> annotated
image + JSON + YAML + fence mask, all returned for display on one page. No
new recognition logic lives here; see src/pipeline.py.

Fence detection (SegFormer) is required for a web analysis to succeed: a
YOLO-only result is never reported back as a completed analysis. If the
fence model can't be loaded or inference fails, /api/analyze responds with
503 rather than silently falling back (see PipelineOptions.require_fence
and FenceDetectionError in src/pipeline.py). This differs from detect.py's
CLI, which still falls back to YOLO-only with a printed warning.

Run locally with:

    uvicorn web.app:app --reload

Uploaded images and generated outputs are written to a per-run temporary
directory and swept on a simple TTL (CITY_TECHNO_VISION_RUN_TTL_SECONDS,
default 30 minutes) so they don't accumulate without bound. There is no
database, login, or history -- see README / Issue #14 for scope.
"""

from __future__ import annotations

import io
import logging
import os
import shutil
import tempfile
import time
import uuid
from pathlib import Path

import cv2
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError

from src.export import write_json, write_yaml
from src.pipeline import FenceDetectionError, PipelineOptions, run_pipeline

logger = logging.getLogger("city_techno_vision.web")

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
CONTENT_TYPE_TO_EXTENSION = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}
MAX_UPLOAD_BYTES = 20 * 1024 * 1024  # 20MB, generous for a single street photo

RUNS_DIR = Path(os.environ.get("CITY_TECHNO_VISION_RUNS_DIR") or Path(tempfile.gettempdir()) / "city-techno-vision-runs")
RUN_TTL_SECONDS = int(os.environ.get("CITY_TECHNO_VISION_RUN_TTL_SECONDS", 30 * 60))

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="City Techno Vision")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


def _cleanup_old_runs() -> None:
    """Delete run directories older than RUN_TTL_SECONDS.

    A best-effort sweep on each request is enough for this MVP (no DB, no
    background scheduler) -- it just keeps the temp directory from growing
    without bound across many uploads.
    """
    if not RUNS_DIR.is_dir():
        return
    cutoff = time.time() - RUN_TTL_SECONDS
    for run_dir in RUNS_DIR.iterdir():
        try:
            if run_dir.is_dir() and run_dir.stat().st_mtime < cutoff:
                shutil.rmtree(run_dir, ignore_errors=True)
        except OSError:
            continue


def _run_dir(run_id: str) -> Path:
    run_dir = (RUNS_DIR / run_id).resolve()
    if RUNS_DIR.resolve() not in run_dir.parents or not run_dir.is_dir():
        raise HTTPException(status_code=404, detail="run not found (it may have expired)")
    return run_dir


def _serve_glob(run_dir: Path, pattern: str, download_name: str) -> FileResponse:
    matches = sorted(run_dir.glob(pattern))
    if not matches:
        raise HTTPException(status_code=404, detail="asset not found")
    return FileResponse(matches[0], filename=download_name)


@app.post("/api/analyze")
async def analyze(image: UploadFile = File(...)) -> JSONResponse:
    _cleanup_old_runs()

    suffix = Path(image.filename or "").suffix.lower()
    if image.content_type not in ALLOWED_CONTENT_TYPES and suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="unsupported file type; use JPG, PNG, or WEBP")

    data = await image.read()
    if not data:
        raise HTTPException(status_code=400, detail="empty file")
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=400, detail="file too large (limit 20MB)")

    try:
        with Image.open(io.BytesIO(data)) as pil_image:
            pil_image.verify()
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="could not read image file")

    if suffix not in ALLOWED_EXTENSIONS:
        suffix = CONTENT_TYPE_TO_EXTENSION.get(image.content_type, ".jpg")

    run_id = uuid.uuid4().hex
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    original_path = run_dir / f"original{suffix}"
    original_path.write_bytes(data)

    try:
        # Fence detection is required, not an optional extra: a YOLO-only
        # result must not be reported back as a complete analysis.
        pipeline_result = run_pipeline(original_path, PipelineOptions(require_fence=True))
    except ValueError as exc:
        shutil.rmtree(run_dir, ignore_errors=True)
        raise HTTPException(status_code=400, detail=str(exc))
    except FenceDetectionError as exc:
        logger.warning("fence detection unavailable for run %s: %s", run_id, exc)
        shutil.rmtree(run_dir, ignore_errors=True)
        raise HTTPException(
            status_code=503,
            detail=(
                "analysis could not be completed: fence detection is required "
                f"but unavailable ({exc})"
            ),
        )
    except Exception:
        logger.exception("analysis failed for run %s", run_id)
        shutil.rmtree(run_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail="analysis failed; please try a different image")

    annotated_path = run_dir / f"annotated{suffix}"
    cv2.imwrite(str(annotated_path), pipeline_result.annotated_image)

    json_path = run_dir / "detections.json"
    yaml_path = run_dir / "detections.yaml"
    write_json(pipeline_result.result, json_path)
    write_yaml(pipeline_result.result, yaml_path)

    fence_mask_url = None
    if pipeline_result.fence_mask is not None:
        fence_mask_path = run_dir / "fence_mask.png"
        cv2.imwrite(str(fence_mask_path), (pipeline_result.fence_mask * 255).astype("uint8"))
        fence_mask_url = f"/api/runs/{run_id}/fence_mask"

    return JSONResponse(
        {
            "run_id": run_id,
            "result": pipeline_result.result,
            "json_text": json_path.read_text(encoding="utf-8"),
            "yaml_text": yaml_path.read_text(encoding="utf-8"),
            "warnings": pipeline_result.warnings,
            "assets": {
                "original": f"/api/runs/{run_id}/original",
                "annotated": f"/api/runs/{run_id}/annotated",
                "json": f"/api/runs/{run_id}/json",
                "yaml": f"/api/runs/{run_id}/yaml",
                "fence_mask": fence_mask_url,
            },
        }
    )


@app.get("/api/runs/{run_id}/original")
def get_original(run_id: str) -> FileResponse:
    return _serve_glob(_run_dir(run_id), "original.*", "original")


@app.get("/api/runs/{run_id}/annotated")
def get_annotated(run_id: str) -> FileResponse:
    return _serve_glob(_run_dir(run_id), "annotated.*", "annotated")


@app.get("/api/runs/{run_id}/fence_mask")
def get_fence_mask(run_id: str) -> FileResponse:
    return _serve_glob(_run_dir(run_id), "fence_mask.png", "fence_mask.png")


@app.get("/api/runs/{run_id}/json")
def get_json(run_id: str) -> FileResponse:
    path = _run_dir(run_id) / "detections.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="asset not found")
    return FileResponse(path, media_type="application/json", filename="detections.json")


@app.get("/api/runs/{run_id}/yaml")
def get_yaml(run_id: str) -> FileResponse:
    path = _run_dir(run_id) / "detections.yaml"
    if not path.exists():
        raise HTTPException(status_code=404, detail="asset not found")
    return FileResponse(path, media_type="application/x-yaml", filename="detections.yaml")
