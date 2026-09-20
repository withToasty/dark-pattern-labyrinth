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

初回実行時に、モデルの重み（`yolov8n.pt`、COCOデータセットで学習済み・80クラス）が
自動でダウンロードされる。

## 使い方

```
python detect.py --image path/to/photo.jpg --output-dir output/
```

オプション：

| フラグ | デフォルト | 説明 |
| --- | --- | --- |
| `--image` | (必須) | 入力画像のパス |
| `--output-dir` | `output/` | 出力先ディレクトリ |
| `--model` | `yolov8n.pt` | 使用するUltralytics YOLOモデル/重みファイル |
| `--conf` | `0.25` | 検出の信頼度しきい値 |

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

## スコープ外

このリポジトリの `Tk-work` フォルダには一切触れていない（読み込み・編集・書き込み・
移動・削除・追加のいずれも行っていない）。このプロジェクトは完全に独立したフォルダ
として作成している。
