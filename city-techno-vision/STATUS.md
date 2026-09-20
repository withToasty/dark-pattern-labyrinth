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
- semantic segmentation mask → threshold → connected components → bbox
- fence を既存 `Detection` 形式へ変換
- 通常 detector と fence detector の結果を merge
- ID の振り直し
- `fence_mask.png` のデバッグ出力
- 合成 mask テスト
- stub model / processor を使った `predict_mask()` の前後処理テスト

## 採用モデル

`nvidia/segformer-b0-finetuned-cityscapes-1024-1024`

- Hugging Face transformers
- Apache-2.0
- SegFormer B0 / Cityscapes 19-class
- fence = class id 4
- 追加 fine-tuning なしでまず検証
- CPUで最低限のテスト可能

PR #11 ではこのモデル向けに:
- `SegformerImageProcessor`
- `SegformerForSemanticSegmentation`
- logits の bilinear upsample
- softmax
- fence class channel 抽出

まで実装済み。

## 確認済み

- `mask_to_detections` — 合成マスクで pass
- `merge_detections` — pass
- `predict_mask()` の upsample / class selection — stubで pass
- `--fence-model` なしの通常CLI — 従来通り動作
- fence model load失敗時 — 明確にエラー終了
- Open Images V7 重み取得 — Claude sandboxから成功

## 現在のブロッカー

Claude sandbox では `huggingface.co` が proxy 403 で拒否されるため、
SegFormer の実重みを取得できない。

そのため未確認:
- 実モデル + 実写真での fence 推論品質
- 実際の fence probability
- threshold 0.5 が適切か
- 実写真で生成される fence bbox

これはコード設計上のブロックではなく、実行環境のネットワーク制限。

## 次のアクション

GitHub Actions を使い、Hugging Face へ到達できる環境で実モデルを取得して
PR #11 を end-to-end 検証する。

現在の作業指示は `TASK.md` を正本とする。

実モデル結果を見るまでは:
- 別モデル比較をしない
- fine-tuningしない
- thresholdを先回りで調整しない

## 制約

- `Tk-work` に触れない。
- 音生成側へ進まない。
- 既存 JSON/YAML schema を壊さない。
- Open Images V7 の通常 detector を置き換えない。
- PR #11 を実モデル検証前に main へ merge しない。

## 正本

現在の作業指示: `TASK.md`
恒久ルール: ルート `CLAUDE.md`
過去の `CLAUDE_FENCE_TASK.md` は履歴として残すが通常は読まない。
