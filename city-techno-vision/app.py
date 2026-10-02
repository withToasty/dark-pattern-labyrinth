#!/usr/bin/env python3
"""Local web page: upload an image, run detect.py on it, and see the results.

    pip install -r requirements.txt flask
    python app.py            # then open http://127.0.0.1:5000

Each upload is processed by the same detect.py CLI, so the page always shows
exactly what the command line would produce.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory

ROOT = Path(__file__).resolve().parent
RUNS = Path(tempfile.gettempdir()) / "city-techno-vision-runs"
RUNS.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 30 * 1024 * 1024

PAGE = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>City Techno Vision</title>
<style>
body{font-family:system-ui,sans-serif;max-width:960px;margin:0 auto;padding:16px;background:#111;color:#eee}
h1{font-size:20px} .row{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin:12px 0}
button{padding:8px 16px;font-size:15px} img{max-width:100%;border-radius:6px}
table{border-collapse:collapse;width:100%;margin-top:8px} td,th{padding:4px 8px;border-bottom:1px solid #333;text-align:left}
.bar{height:8px;background:#4ade80;border-radius:4px} .muted{color:#999;font-size:13px}
pre{background:#1b1b1b;padding:8px;overflow:auto;max-height:300px;font-size:12px} .err{color:#f87171;white-space:pre-wrap}
</style></head><body>
<h1>City Techno Vision — 画像認識テスト</h1>
<form id="f" class="row">
  <input type="file" name="image" accept="image/*" required>
  <label>信頼度しきい値 <input type="number" name="conf" value="0.15" min="0.01" max="0.95" step="0.01" style="width:70px"></label>
  <label>レンズ <select name="lens_mode"><option>auto</option><option>ultrawide</option><option>standard</option></select></label>
  <button>認識する</button>
</form>
<div id="status" class="muted"></div><div id="out"></div>
<script>
const f=document.getElementById('f'),st=document.getElementById('status'),out=document.getElementById('out');
f.addEventListener('submit',async e=>{
  e.preventDefault(); out.innerHTML=''; st.textContent='認識中…（初回はモデルのダウンロードで時間がかかります）';
  const r=await fetch('/api/detect',{method:'POST',body:new FormData(f)});
  const d=await r.json(); st.textContent='';
  if(!r.ok){out.innerHTML='<div class="err"></div>';out.firstChild.textContent=d.error;return;}
  const dets=d.result.detections, h=(d.result.scene_geometry||{}).horizon;
  const counts={}; dets.forEach(x=>counts[x.label]=(counts[x.label]||0)+1);
  const esc=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
  let html='<img src="'+d.image_url+'"><p><b>'+dets.length+' 件検出</b> — '+
    Object.entries(counts).map(([k,v])=>esc(k)+' ×'+v).join(', ')+'</p>';
  html+='<p class="muted">ホライゾン: '+(h?(h.detected?'検出 (信頼度 '+h.confidence.toFixed(2)+')':'未検出 ('+esc(h.rejection_reason||'')+')'):'—')+'</p>';
  html+='<table><tr><th>ラベル</th><th>信頼度</th><th></th></tr>'+dets.slice().sort((a,b)=>b.confidence-a.confidence)
    .map(x=>'<tr><td>'+esc(x.label)+(x.group?' <span class="muted">('+esc(x.group)+')</span>':'')+'</td><td>'+x.confidence.toFixed(2)+
      '</td><td style="width:40%"><div class="bar" style="width:'+Math.round(x.confidence*100)+'%"></div></td></tr>').join('')+'</table>';
  html+='<details><summary>JSON</summary><pre>'+esc(JSON.stringify(d.result,null,2))+'</pre></details>';
  out.innerHTML=html;
});
</script></body></html>"""


@app.get("/")
def index():
    return PAGE


@app.post("/api/detect")
def detect():
    upload = request.files.get("image")
    if upload is None or not upload.filename:
        return jsonify(error="image is required"), 400
    try:
        conf = float(request.form.get("conf", "0.15"))
    except ValueError:
        return jsonify(error="conf must be a number"), 400
    lens_mode = request.form.get("lens_mode", "auto")
    if lens_mode not in ("auto", "ultrawide", "standard"):
        return jsonify(error="invalid lens_mode"), 400

    run_id = uuid.uuid4().hex
    run_dir = RUNS / run_id
    run_dir.mkdir()
    suffix = Path(upload.filename).suffix.lower()
    if suffix not in (".jpg", ".jpeg", ".png", ".webp", ".bmp"):
        suffix = ".jpg"
    image_path = run_dir / f"input{suffix}"
    upload.save(image_path)

    proc = subprocess.run(
        [sys.executable, str(ROOT / "detect.py"), "--image", str(image_path),
         "--output-dir", str(run_dir / "out"), "--conf", str(conf), "--lens-mode", lens_mode],
        cwd=ROOT, capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return jsonify(error=(proc.stderr or proc.stdout)[-2000:]), 500
    result = json.loads((run_dir / "out" / "detections.json").read_text(encoding="utf-8"))
    return jsonify(result=result, image_url=f"/runs/{run_id}/input_detected{suffix}")


@app.get("/runs/<run_id>/<name>")
def run_file(run_id: str, name: str):
    if not run_id.isalnum():
        abort(404)
    return send_from_directory(RUNS / run_id / "out", name)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
