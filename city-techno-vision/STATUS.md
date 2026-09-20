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

- 通常の物体検出: Ultralytics YOLO + `yolov8n-oiv7.pt` (Open Images V7)
- bbox付き画像
- `detections.json`
- `detections.yaml`
- YOLO-World 用 open-vocabulary 経路
- GitHub Actions の手動検証 workflow: `.github/workflows/fence-validation.yml`

## fence 実装

PR #11:
`city-techno-vision: add fence recognition via semantic segmentation`

状態:
- OPEN
- main 未反映
- 現在 mergeable=false のため、merge前にmainとの競合整理が必要

実装済み:
- `FenceDetector`
- semantic segmentation mask → threshold → connected components → bbox
- fence を既存 `Detection` 形式へ変換
- 通常 detector と fence detector の結果を merge
- ID の振り直し
- `fence_mask.png`
- 合成 mask テスト
- stub model / processor を使った `predict_mask()` テスト

## 採用モデル

`nvidia/segformer-b0-finetuned-cityscapes-1024-1024`

- Hugging Face transformers
- Apache-2.0
- SegFormer B0 / Cityscapes 19-class
- fence = class id 4
- fine-tuningなしで検証

## 実モデル検証 — 成功

GitHub Actions run #2:
- run id: `35527951489`
- branch: `claude/fence-task-implementation-85wezz`
- real test image: `city-techno-vision/tests/fixtures/kobe_fence_test.jpg`（一時fixture）
- conclusion: success

確認済み:
- 依存関係 install
- Hugging Face から実モデル取得
- Open Images V7 detector 実行
- SegFormer fence inference 実行
- fence mask 生成
- fence bbox 生成
- 通常 detections と merge
- annotated image 生成
- JSON / YAML 生成
- GitHub Actions artifact upload

実測:
- total detections: 6
- fence detections: 2
- 主な fence bbox:
  - confidence 0.8991
  - minx 0 / maxx 2541
  - miny 1151 / maxy 1446
- 小さい第2 fence component:
  - confidence 0.5982
  - minx 856 / maxx 958
  - miny 1150 / maxy 1166

artifact:
- `fence-validation-output`
- `photo_detected.jpg`
- `fence_mask.png`
- `detections.json`
- `detections.yaml`

視覚確認でも、写真下部の長い柵・フェンス領域を主要bboxとして検出できている。

## 判断

「実モデルで fence が実写真から検出され、既存 JSON/YAML/bbox 出力へ統合される」
という今回の Definition of Done は達成。

第2の小さい fence component はあるが、初回1枚だけを見て threshold や後処理を最適化しない。
現時点ではMVPとして許容し、必要なら複数画像での挙動を見て後から調整する。

## 次のアクション

新機能追加ではなく PR #11 のクリーンアップ:

1. 一時テスト画像をPRブランチから削除する
2. main の最新変更をPR #11ブランチへ取り込み、競合を解消する
3. 既存テストを再実行する
4. PR #11 が mergeable になることを確認する
5. 変更内容を短く報告する
6. ユーザー確認前にPR #11をmergeしない

現在の作業指示は `TASK.md`。

## 制約

- `Tk-work` に触れない
- 音生成側へ進まない
- JSON/YAML schema を壊さない
- Open Images V7 detector を置き換えない
- 不要なthreshold調整・fine-tuning・別モデル比較をしない
- PR #11を勝手にmergeしない

## 正本

- 恒久ルール: ルート `CLAUDE.md`
- 現在地: `city-techno-vision/STATUS.md`
- 現在タスク: `city-techno-vision/TASK.md`
