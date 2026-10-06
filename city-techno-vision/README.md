# city-techno-vision

City Techno プロジェクトの「画像認識」部分のみを実装したもの。

やること：

```
画像
 ↓
Open Images YOLO + YOLO-World + Cityscapes SegFormer + 音楽用リファレンス・ホライゾン推定
 ↓
枠線・ホライゾン付き画像 ＋ JSON / YAML
```

音（物体と音の対応、BPM、音程、リズム、MIDI/音声生成など）への変換は
別プロジェクトの責務であり、このコードには一切含まれていない。

## セットアップ

```
pip install -r requirements.txt
```

初回実行時に、主検出器 `yolov8n-oiv7.pt`（Open Images V7・601クラス）、補助の `yolov8s-worldv2.pt`（open vocabulary）、および Cityscapes SegFormer の重みが必要に応じて自動ダウンロードされる。

## 使い方

```
python detect.py --image path/to/photo.jpg --output-dir output/
```

オプション：

| フラグ | デフォルト | 説明 |
| --- | --- | --- |
| `--image` | (必須) | 入力画像のパス |
| `--output-dir` | `output/` | 出力先ディレクトリ |
| `--model` | `yolov8n-oiv7.pt` | 使用するUltralytics YOLOモデル/重みファイル |
| `--conf` | `0.05` | Open Images YOLOの信頼度しきい値。音素材の取りこぼしを減らすため低めに設定 |
| `--world-model` | `yolov8s-worldv2.pt` | 補助のopen-vocabulary検出器。空文字で無効化 |
| `--world-conf` | `0.05` | YOLO-Worldの信頼度しきい値 |
| `--classes` | 街向け語彙 | YOLO-Worldで探す対象をカンマ区切りで指定。省略時は車両・道路・高架・ガードレール・建物・看板・自然物などの広い語彙を使う |
| `--fence-model` | `nvidia/segformer-b0-finetuned-cityscapes-1024-1024` | 互換性のため名称は維持。現在はfenceだけでなく road / sidewalk / building / wall / pole / vegetation / terrain / sky も抽出する |
| `--seg-conf` | `0.35` | SegFormerのクラス確率しきい値 |
| `--seg-classes` | 9クラス | SegFormerでbbox化するCityscapesクラスを指定 |
| `--lens-mode` | `auto` | `auto` / `ultrawide` / `standard`。`auto` はEXIFのレンズ情報を使い、`ultrawide` は汎用の超広角近似を明示的に有効化する |
| `--curve-strength` | (なし) | 曲線近似の強さを手動指定。常に approximation として出力し、実測キャリブレーションとは扱わない |
| `--no-horizon` | off | 幾何学的な地平線推定を無効化する |

## モデルについて（Open Images V7 vs COCO）

デフォルトの`yolov8n-oiv7.pt`はOpen Images V7で学習済み・601クラス。
COCO(80クラス、`yolov8n.pt`)と比べて、日常的な物体はほぼそのまま検出でき、
街の風景を構成する要素（building, skyscraper, tree, window, door, billboard,
street light, traffic signなど）が追加で検出できる。

実際に調べた重なり具合：

- COCOの80クラスのうち66クラスはOpen Images V7にも同じ名前で存在する
- 6クラスは名前が違うだけで実質同じ（例: `tv` → `Television`、`remote` → `Remote control`）
- 8クラスはOpen Images V7に存在しない（donut, frisbee, potted plant, skis,
  sports ball, cup, cow(→`Cattle`という別名で存在), cell phone）

### Cityscapes セマンティックセグメンテーション

`fence` のような細長い構造物だけでなく、道路・歩道・建物・空など「面として存在する景色」を通常の物体検出だけに任せないため、`src/fence_detector.py` の `CityscapesDetector` でセマンティックセグメンテーションを使う。従来コードとの互換性のため `FenceDetector` 名も残している。

採用モデル:

`nvidia/segformer-b0-finetuned-cityscapes-1024-1024`

Cityscapes 19-class taxonomy から、デフォルトでは `road / sidewalk / building / wall / fence / pole / vegetation / terrain / sky` の確率マスクを1回の推論で取得し、各クラスごとに

```text
fence probability mask
→ threshold
→ connected components
→ bbox
→ Detection(label="fence", ...)
```

として既存の JSON / YAML 出力に統合する。

実行例:

```
python detect.py --image photo.jpg \
  --fence-model nvidia/segformer-b0-finetuned-cityscapes-1024-1024
```

実モデル + 実写真による end-to-end 検証は GitHub Actions で成功済み。
通常YOLO検出、SegFormer推論、`fence_mask.png`、fence bbox、
annotated image、JSON/YAML出力まで確認している。

### リファレンス・ホライゾン

`src/horizon.py` で、画像内の長い線分から複数のホライゾン候補を作る。目的は測量上の真値ではなく、物体からの距離などを音へ変換するときに違和感の少ない `musical_reference` を得ること。
都市写真では縦方向・横方向の消失点を使う候補と、2つの横方向消失点を使う候補を評価し、自然な候補だけを採用する。

```text
image
→ Canny
→ Hough line segments
→ dominant vanishing point A
→ dominant vanishing point B
→ horizon line
```

外部AIモデルは使わず、OpenCVのみで動く。
道路・建物など直線が多い都市景観を主対象とし、
十分な幾何情報がない場合は無理に線を作らず `detected: false` を返す。

さらに、候補が数学的に成立してもそのまま採用しない。以下のゲートで「音楽用の基準線として自然か」を評価する。

- 支持線が画像幅の広い範囲に分散しているか
- 一部の建物・道路だけに局所化していないか
- ホライゾンの大部分が画像内にあるか
- 傾きが極端でないか
- 既存の幾何 confidence と上記条件を合わせた `reference_score`

不採用時は `detected: false` とし、`rejection_reason` に
`excessive_tilt` / `mostly_out_of_frame` /
`insufficient_spatial_support` / `localized_support` /
`low_reference_score` などを残す。

出力の直下（`detected` / `method` / `confidence` / `supporting_lines` /
`vanishing_points`）に加えて、地平線そのものは `rectified`（幾何学的な直線）と
`distorted`（広角写真での歪み込みを想定した曲線）の二層で持つ。

`rectified`（直線、従来のline情報）:

- `type`: `"line"`
- `left_y`: 画像左端での地平線y座標
- `right_y`: 画像右端での地平線y座標
- `center_y`: 画像中央での地平線y座標
- `center_y_normalized`: 高さを画像高で0〜1相当に正規化した値
- `slope`: 地平線の傾き
- `angle_deg`: 傾きを角度で表した値

`distorted`（曲線、広角写真の歪みを想定した近似）:

- `type`: `"curve"`
- `sampling`: `"polyline"`（`points` は折れ線として補間する前提）
- `points`: `[x, y]` の点列（現在は7点）
- `curve_strength`: 曲がりの強さ（画像高に対する比率）
- `distortion_source`: `exif_heuristic` / `manual_lens_mode` / `manual_curve_strength` など
- `distortion_model`: 現在は `parabolic_approximation`
- `is_approximation`: 実測キャリブレーションではない場合 `true`
- `basis`: その近似を採用した根拠
- `center_y` / `center_y_normalized`: 画像水平中心でのy座標

重要: EXIFや手動指定など、歪みを使う根拠がない画像では `distorted: null` とし、固定値で勝手に曲線を作らない。
`--lens-mode ultrawide` またはEXIFから超広角と判断できた場合にのみ、汎用の放物線近似を出す。これは実レンズのキャリブレーション値ではなく、必ず `is_approximation: true` として区別する。

トップレベルの主な出力：

- `role`: 現在は `musical_reference`
- `confidence`: 幾何学的な線分支持率などから計算した信頼度
- `reference_score`: 音楽用基準線としての自然さを含む採用スコア
- `rejection_reason`: 候補を棄却した場合の理由
- `spatial_support_span` / `spatial_support_bins`: 支持線が画像横方向にどれだけ広がっているか
- `in_frame_fraction`: 候補線のうち画像内に収まる割合
- `vanishing_points`: 検証用の消失点座標

## 検出対象を増やす（open-vocabulary detection）

通常実行でも Open Images V7 の固定601クラスに加えて YOLO-World を補助的に実行する。
`--classes` を省略すると `src/detector.py` の `DEFAULT_CITY_CLASSES` を使い、
car / bus / motorcycle / person に加えて road / curb / guardrail / railing /
bridge / overpass / traffic light / utility pole / building / window / billboard /
tree / sky など、街から音素材を拾うための広い語彙を検索する。

独自語彙に絞る場合:

```
python detect.py --image photo.jpg \
  --classes "overpass,guardrail,traffic light,car,bus,puddle"
```

YOLO-Worldを使わずOpen Images側だけ試したい場合は `--world-model ""` とする。

## 出力

`--output-dir` に以下を出力する。

- `<元画像名>_detected.<拡張子>`
- `detections.json`
- `detections.yaml`
- fence検出時: `fence_mask.png`

### 車系ラベルの扱い

Open Images V7 では同じ車両が `Car` ではなく `Land vehicle` として強く検出されることがある。元の `label` はそのまま保持しつつ、`Car` / `Land vehicle` / `Truck` / `Bus` / `Motorcycle` は出力時に `group: road_vehicle` を追加する。音生成側は必要ならこの `group` を使って同じ車系として扱える。

### 座標系

- 原点は画像左上
- x は右方向に増加
- y は下方向に増加

### JSON / YAML の形式

```json
{
  "image": {
    "filename": "sample.jpg",
    "width": 1920,
    "height": 1080,
    "camera": {
      "make": "Apple",
      "model": "iPhone",
      "lens_model": "Ultra Wide Camera",
      "focal_length_mm": 2.2,
      "focal_length_35mm": 13.0,
      "orientation": 1,
      "lens_mode": "ultrawide",
      "lens_mode_effective": "ultrawide",
      "lens_mode_source": "exif"
    }
  },
  "detections": [
    {
      "id": 1,
      "label": "Land vehicle",
      "group": "road_vehicle",
      "confidence": 0.19,
      "source": "yolo_oiv7",
      "minx": 210,
      "maxx": 540,
      "miny": 620,
      "maxy": 850
    }
  ],
  "scene_geometry": {
    "horizon": {
      "detected": true,
      "method": "vertical_guided_single_vp",
      "role": "musical_reference",
      "confidence": 0.81,
      "candidate_detected": true,
      "reference_score": 0.76,
      "spatial_support_span": 0.68,
      "spatial_support_bins": 3,
      "in_frame_fraction": 1.0,
      "rejection_reason": null,
      "supporting_lines": 14,
      "vanishing_points": [
        {"x": -1120.4, "y": 481.5, "supporting_lines": 7},
        {"x": 2540.1, "y": 516.7, "supporting_lines": 7}
      ],
      "rectified": {
        "type": "line",
        "center_y": 501.6,
        "center_y_normalized": 0.4644,
        "left_y": 492.3,
        "right_y": 510.8,
        "slope": 0.0096,
        "angle_deg": 0.55
      },
      "distorted": {
        "type": "curve",
        "sampling": "polyline",
        "points": [
          [0.0, 495.4],
          [320.0, 499.5],
          [640.0, 501.2],
          [960.0, 501.6],
          [1280.0, 501.2],
          [1600.0, 499.5],
          [1919.0, 495.4]
        ],
        "curve_strength": 0.015,
        "distortion_source": "exif_heuristic",
        "distortion_model": "parabolic_approximation",
        "is_approximation": true,
        "basis": "EXIF focal_length_35mm=13",
        "center_y": 501.6,
        "center_y_normalized": 0.4644
      }
    }
  }
}
```

## 構成

```
city-techno-vision/
  detect.py
  src/
    camera_metadata.py
    detector.py
    fence_detector.py
    horizon.py
    visualize.py
    export.py
  tests/
    test_camera_metadata.py
    test_fence_detector.py
    test_horizon.py
  requirements.txt
```

## 既知の制約

地平線推定は、道路・建物など複数方向の直線がある都市景観で最も安定する。
森・空・海だけの画像や、直線がほぼない画像では `detected: false` になることがある。
将来、iPhone専用カメラで撮影時の姿勢センサー値を保存できれば、
そちらを優先し、この画像推定をfallbackにする想定。

YOLO-World と SegFormer は初回に追加モデルを取得するため、ネットワーク制限のある実行環境では補助パスが利用できないことがある。Open Images YOLOの結果は独立して保持し、補助モデルが利用できる環境では結果を同じ detection list に追加する。SegFormerの実モデル + 実写真推論はGitHub Actions上で確認済み。

## スコープ外

`Tk-work` には触れない。
音生成、BPM、MIDI、物体→音のマッピングは別プロジェクトで扱う。
