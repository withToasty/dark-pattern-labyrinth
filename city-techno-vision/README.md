# city-techno-vision

City Techno プロジェクトの「画像認識」部分のみを実装したもの。

やること：

```
画像
 ↓
物体検出 + 幾何学的な地平線推定
 ↓
枠線・地平線付き画像 ＋ JSON / YAML
```

音（物体と音の対応、BPM、音程、リズム、MIDI/音声生成など）への変換は
別プロジェクトの責務であり、このコードには一切含まれていない。

## セットアップ

```
pip install -r requirements.txt
```

初回実行時に、モデルの重み（デフォルトは`yolov8n-oiv7.pt`、Open Images V7データセットで
学習済み・601クラス）が自動でダウンロードされる。

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
| `--conf` | `0.15` | 検出の信頼度しきい値。神戸の実写検証では0.25だと車系が落ち、0.15で2台の `Land vehicle` を保持できた |
| `--classes` | (なし) | 検出したい対象をカンマ区切りで指定。open-vocabularyモデル（`--model`に`world`を含むもの）でのみ有効 |
| `--fence-model` | `nvidia/segformer-b0-finetuned-cityscapes-1024-1024` | fence用セマンティックセグメンテーションモデル。通常実行でも自動で fence 領域を検出し、YOLOの結果とマージする |
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

### fence の検出

`fence` は通常の物体検出だけでは安定しないため、
`src/fence_detector.py` の `FenceDetector` でセマンティックセグメンテーションを使う。

採用モデル:

`nvidia/segformer-b0-finetuned-cityscapes-1024-1024`

Cityscapes 19-class taxonomy の `fence` (class id 4) の確率マスクを取得し、

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

### 幾何学的な地平線

`src/horizon.py` で、画像内の長い線分から消失点を推定し、
2つの支配的な消失点を結んで幾何学的な地平線を求める。

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

主な出力：

- `left_y`: 画像左端での地平線y座標
- `right_y`: 画像右端での地平線y座標
- `center_y`: 画像中央での地平線y座標
- `center_y_normalized`: 高さを画像高で0〜1相当に正規化した値
- `slope`: 地平線の傾き
- `angle_deg`: 傾きを角度で表した値
- `confidence`: 線分の支持率などから計算した信頼度
- `vanishing_points`: 検証用の消失点座標

## 検出対象を増やす（open-vocabulary detection）

さらに独自の単語を検出したい場合は、YOLO-World を使う。

```
python detect.py --image photo.jpg --model yolov8s-worldv2.pt
```

`--classes`を省略すると、`src/detector.py`の`DEFAULT_CITY_CLASSES`
（街の風景向け単語リスト）が使われる。

```
python detect.py --image photo.jpg --model yolov8s-worldv2.pt \
  --classes "building,car,tree"
```

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
    "height": 1080
  },
  "detections": [
    {
      "id": 1,
      "label": "Land vehicle",
      "group": "road_vehicle",
      "confidence": 0.19,
      "minx": 210,
      "maxx": 540,
      "miny": 620,
      "maxy": 850
    }
  ],
  "scene_geometry": {
    "horizon": {
      "detected": true,
      "method": "line_vanishing_points",
      "confidence": 0.81,
      "left_y": 492.3,
      "right_y": 510.8,
      "center_y": 501.6,
      "center_y_normalized": 0.4644,
      "slope": 0.0096,
      "angle_deg": 0.55,
      "supporting_lines": 14,
      "vanishing_points": [
        {"x": -1120.4, "y": 481.5, "supporting_lines": 7},
        {"x": 2540.1, "y": 516.7, "supporting_lines": 7}
      ]
    }
  }
}
```

## 構成

```
city-techno-vision/
  detect.py
  src/
    detector.py
    fence_detector.py
    horizon.py
    visualize.py
    export.py
  tests/
    test_fence_detector.py
    test_horizon.py
  requirements.txt
```

## 既知の制約

地平線推定は、道路・建物など複数方向の直線がある都市景観で最も安定する。
森・空・海だけの画像や、直線がほぼない画像では `detected: false` になることがある。
将来、iPhone専用カメラで撮影時の姿勢センサー値を保存できれば、
そちらを優先し、この画像推定をfallbackにする想定。

`--classes`（YOLO-World）は、開発時のサンドボックスではCLIPの初回取得先が
ネットワークポリシーでブロックされ、実検出までは未確認。

fence用SegFormerはClaude sandboxではHugging Faceへの接続がブロックされたが、
GitHub Actions上で実モデル + 実写真の推論を確認済み。

## スコープ外

`Tk-work` には触れない。
音生成、BPM、MIDI、物体→音のマッピングは別プロジェクトで扱う。
