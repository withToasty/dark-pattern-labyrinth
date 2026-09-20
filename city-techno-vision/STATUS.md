# STATUS — city-techno-vision

最終更新: 2026-09-21 (JST)

## 目的

City Techno の画像認識部分。

```text
画像
→ 物体・領域の認識
→ bbox付き画像
→ JSON / YAML
```

音生成、BPM、MIDI、物体→音のマッピングは別プロジェクトの責務。

## main で動いているもの

- `city-techno-vision/` は独立したプロジェクトとして存在。
- 通常の物体検出は Ultralytics YOLO + `yolov8n-oiv7.pt` (Open Images V7)。
- 実画像で通常検出、bbox描画、JSON/YAML出力まで確認済み。
- 出力 Detection:
  - `id`
  - `label`
  - `confidence`
  - `minx`
  - `maxx`
  - `miny`
  - `maxy`
- YOLO-World 用の open-vocabulary 経路も実装済み。
- `fence` は通常の物体検出だけでは安定しないため、別経路で扱う方針。

## fence の現在地

PR #11:
`city-techno-vision: add fence recognition via semantic segmentation`

状態:
- OPEN
- mergeable
- main 未反映

PR #11 で実装済み:
- `FenceDetector`
- セグメンテーション mask → threshold → connected components → bbox
- fence を既存 `Detection` 形式へ変換
- 通常 detector と fence detector の結果を merge
- ID の振り直し
- `fence_mask.png` のデバッグ出力
- 合成 mask を使ったテスト

未確認:
- 実際の学習済みセグメンテーションモデルを使った fence 推論
- 実写真での fence 検出品質
- 実モデル固有の preprocessing / normalization / output shape / class id への適合

## 現在の判断

次は追加学習ではない。

まず公開済みの fence クラス対応セマンティックセグメンテーションモデルを1つ選び、
PR #11 の経路へ実接続して、実写真で end-to-end 検証する。

それで不十分な場合にのみ、
1. preprocessing / threshold 等の調整
2. fine-tuning
3. エッジ・格子パターン等の補助的画像処理

を検討する。

## 制約

- `Tk-work` に触れない。
- 音生成側へ進まない。
- 既存 JSON/YAML schema を壊さない。
- Open Images V7 の通常 detector を置き換えない。
- PR #11 を検証前に main へ merge しない。

## 正本

現在の作業指示は `TASK.md`。
過去の `CLAUDE_FENCE_TASK.md` は履歴として残すが、通常は読まなくてよい。
