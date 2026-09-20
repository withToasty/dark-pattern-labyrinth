# city-techno-vision

City Techno プロジェクトの「画像認識」部分のみを実装したもの。

やること：

```
画像
 ↓
物体検出
 ↓
枠線付き画像 ＋ JSON / YAML
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
| `--conf` | `0.25` | 検出の信頼度しきい値 |
| `--classes` | (なし) | 検出したい対象をカンマ区切りで指定。open-vocabularyモデル（`--model`に`world`を含むもの）でのみ有効 |

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

### 検出できないもの：sky / cloud / fence / road

これらは**どの物体検出モデルを選んでも検出できない**。COCOにもOpen Images V7にも
存在しない。理由はモデルの選択の問題ではなく、物体検出というタスクそのものの
性質による：

- car・person・building のような「数えられる、輪郭がはっきりした物」は
  bounding boxと相性がいい
- sky・cloud・fence・road のような「画面のどこまでも広がる背景・領域」は
  そもそも四角い枠で囲む発想に合わない

これらを検出したい場合は、物体検出ではなく**セマンティックセグメンテーション**
（画面を領域ごとに塗り分ける別の手法）が必要になる。今回は一旦保留。

## 検出対象を増やす（open-vocabulary detection）

上記に加えてさらに独自の単語を検出したい場合は、**YOLO-World**という
open-vocabularyモデルを使う。

```
python detect.py --image photo.jpg --model yolov8s-worldv2.pt
```

`--classes`を省略すると、`src/detector.py`の`DEFAULT_CITY_CLASSES`
（街の風景向けに用意した単語リスト）が自動的に使われる。特定の単語だけに
絞りたい場合はこう指定する：

```
python detect.py --image photo.jpg --model yolov8s-worldv2.pt \
  --classes "building,car,tree"
```

**重要**: 検出したい単語を増やすこと自体にコストはかからない（再学習も追加の
ダウンロードも不要。ただの単語リストの書き換え）。ただし初回だけ、単語を理解するための
CLIPテキストエンコーダー（約350MB、`openaipublic.azureedge.net`から取得）を追加で
ダウンロードする必要がある。これは`pip install -r requirements.txt`で入る`clip`パッケージが
初回`--classes`使用時に自動で取得する。

## 出力

`--output-dir` に以下を出力する。

- `<元画像名>_detected.<拡張子>` — bounding box・label・confidenceを描画した画像
- `detections.json`
- `detections.yaml`

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
      "label": "car",
      "confidence": 0.94,
      "minx": 210,
      "maxx": 540,
      "miny": 620,
      "maxy": 850
    }
  ]
}
```

## 構成

```
city-techno-vision/
  detect.py           CLIエントリポイント
  src/
    detector.py        YOLOモデルのラッパー。画像 → Detection のリスト
    visualize.py        Detection を元画像に描画する
    export.py           Detection を JSON / YAML に変換する
  requirements.txt
```

## 既知の制約

`--classes`（open-vocabulary detection）は、開発時のサンドボックス環境では
`openaipublic.azureedge.net`への接続がネットワークポリシーでブロックされていたため、
実際の検出結果までは確認できていない。デフォルトの`yolov8n-oiv7.pt`での検出・描画・
JSON/YAML出力は実画像で動作確認済み。通常のネット環境であれば`--classes`も
問題なく動くはず。

## スコープ外

このリポジトリの `Tk-work` フォルダには一切触れていない（読み込み・編集・書き込み・
移動・削除・追加のいずれも行っていない）。このプロジェクトは完全に独立したフォルダ
として作成している。
