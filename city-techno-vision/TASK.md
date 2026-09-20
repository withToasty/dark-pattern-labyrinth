# TASK — GitHub Actions で実モデル end-to-end 検証

## Goal

Claude sandbox では `huggingface.co` が egress policy で拒否されるため、
PR #11 の実装を変更方針ごと見直すのではなく、GitHub Actions 上で実モデルを取得し、
実写真から fence 検出の end-to-end 動作を確認する。

採用モデルは変更しない:

`nvidia/segformer-b0-finetuned-cityscapes-1024-1024`

今回の目的は「実モデルで本当に fence が取れるか」の検証だけ。

## 最初に読むもの

1. ルート `CLAUDE.md`
2. `city-techno-vision/STATUS.md`
3. この `TASK.md`
4. PR #11 の現在の差分

必要なファイルだけ追加で読む。
リポジトリ全体を再調査しない。

## 実行

1. PR #11 のブランチ上で作業する。
2. `workflow_dispatch` で手動実行できる GitHub Actions workflow を最小構成で追加する。
3. Actions 上で必要な Python 依存関係を install する。
4. Hugging Face から
   `nvidia/segformer-b0-finetuned-cityscapes-1024-1024`
   を実際に取得する。
5. fence が写った実写真1枚を入力して以下を通す。

```text
image
→ normal YOLO
→ SegFormer fence segmentation
→ fence mask
→ fence bbox
→ merge
→ annotated image
→ detections.json
→ detections.yaml
```

6. 以下を Actions artifact として取得できるようにする。
   - `fence_mask.png`
   - bbox付き画像
   - `detections.json`
   - `detections.yaml`
7. workflow log に、最低限以下を出す。
   - 使用モデル
   - fence detection 数
   - 実行成功/失敗
   - 出力先
8. 実モデルの最初の結果を確認するまで、threshold調整・fine-tuning・別モデル比較へ進まない。

## Test image

現在 `city-techno-vision/` には恒久的なテスト用実写真がない。

- 既存の適切な実写真がPRブランチまたは利用可能な場所にあればそれを使う。
- なければ、勝手に無関係な画像を恒久追加しない。
- 画像不足で実行できない場合は、その事実を Blocked として明示する。
- workflow自体は、後からテスト画像を指定・配置して実行しやすい最小構成にする。

## Do not

- 採用モデルを変更しない。
- 新しいモデル比較を始めない。
- fine-tuning を始めない。
- BDD100K 全体を取得しない。
- JSON/YAML schema を変更しない。
- Open Images V7 detector を置き換えない。
- 音生成へ進まない。
- `Tk-work` に触れない。
- 大規模リファクタリングをしない。
- PR #11 を main に merge しない。

## Token / context discipline

- PR #11 と `city-techno-vision` の必要ファイルだけ読む。
- 過去のClaudeチャットを復元しない。
- workflow設計の長い比較説明は不要。
- GitHub Actionsで実検証するための最小変更だけ行う。

## Definition of done

実モデルで以下が確認できれば完了:

```text
実写真
→ pretrained SegFormer
→ fence_mask.png
→ fence bbox
→ normal YOLO と統合
→ annotated image
→ detections.json
→ detections.yaml
→ Actions artifact
```

実写真不足など外部要因で最後まで実行できない場合は、
workflowが準備できた状態と、残る1つのブロッカーを明示する。

## 完了後

```text
Changed:
- ...

Verified:
- ...

Blocked:
- ...   # なければ省略

Next:
- ...
```

結果に応じて `STATUS.md` を更新する。
