# WORLD TO TECHNO

**身の回りの風景・物体・動きを、テクノの素材へ変換する実験プロジェクト。**

Status: EXPERIMENT / v0.1

WITH TOASTの「異なるものを組み合わせる」という思想を、
**CITY / VIDEO / COMPUTER VISION / SOUND / TECHNO** の組み合わせで実装する。

## まず何を作るか

v0.1では、動画そのものを直接解析する前に、
「映像から検出されたもの」のJSONを入力として、

- 何を音にするか
- どの音域・役割に割り当てるか
- どの程度の強さで鳴らすか
- どんなテクノ構成にするか

を自動で決める小さなエンジンを作る。

つまり、

```
video / photo
  ↓
object / scene detection
  ↓
detections.json
  ↓
WORLD TO TECHNO engine
  ↓
arrangement.json
  ↓
sample selection / human finish
  ↓
video + techno
```

## Creative direction

- BGMとして流れて違和感がないことを優先する
- 曲として派手にかっこいいことは必須ではない
- 直訳できるものはなるべく直訳する
- 1つの対象に複数の音候補を持てるようにする
- 最初はサンプル音源を使う
- 8割自動生成 + 人間が仕上げる
- 認識枠は音が鳴る瞬間だけ表示する
- 冒頭で主要音を短く提示し、「TOAST STUDIO」を表示する

## First piece

第一作は**池袋の写真**から始める。
静止画でルールと演出を確認した後、池袋の動画へ発展させる。

詳細: [FIRST_PIECE_IKEBUKURO.md](docs/FIRST_PIECE_IKEBUKURO.md)

## Example

街で検出したもの:

```json
[
  {"label": "car", "confidence": 0.93, "screen_area": 0.24},
  {"label": "bicycle", "confidence": 0.88, "screen_area": 0.08},
  {"label": "construction", "confidence": 0.91, "screen_area": 0.31},
  {"label": "sky", "confidence": 0.99, "screen_area": 0.42}
]
```

変換例:

- car → engine / brake / tire friction
- bicycle → bell / chain / tire roll
- construction → metal hit / drill / machine hum
- sky → ambient / visual space

## Run

Python 3.11+ を想定。

```bash
cd projects/world-to-techno
python -m world_to_techno.cli examples/detections.json
```

出力は `arrangement.json`。

## Current scope

### v0.1
- 検出結果JSONを読む
- ラベルを音の役割へマッピング
- confidence / screen areaから強さを決める
- BPM・レイヤー構成をJSONで出す
- 1対象に複数のサンプル候補を保持する

### 次
- 写真版プロトタイプ
- サンプル音源の選択
- 認識枠の同期表示
- TOAST STUDIOオープニング
- 動画から自動で物体検出
- 対象をフレーム間で追跡
- 実際の音源を生成
- 動画と音を同期して書き出す
- 飯テクノ / 祭り / 風景などへ展開

## Project philosophy

このプロジェクトの目的は、
「AIで自動作曲すること」そのものではない。

**場所・物・動きに元々ある意味や音の連想を、人間のルールと機械認識を使って音楽へ翻訳する。**

完全自動よりも、
「なぜその音になったか」が分かるルールベースを核にする。

## Docs

- [CONCEPT.md](docs/CONCEPT.md)
- [PIPELINE.md](docs/PIPELINE.md)
- [SOUND_MAPPING.md](docs/SOUND_MAPPING.md)
- [DECISIONS.md](docs/DECISIONS.md)
- [FIRST_PIECE_IKEBUKURO.md](docs/FIRST_PIECE_IKEBUKURO.md)

## Ingredients

- Photo / Video
- Computer Vision
- Rule-based Mapping
- Sample Sound
- Human Finishing
- Techno
- City / Food / Festival / Landscape
