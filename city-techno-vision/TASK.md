# TASK — pretrained fence model を実接続して検証する

## Goal

PR #11 にある fence 用セマンティックセグメンテーション経路へ、
実際に利用できる公開済み学習済みモデルを1つ接続し、
実写真から fence → mask → bbox → 既存 JSON/YAML まで通ることを確認する。

## 最初に読むもの

1. ルート `CLAUDE.md`
2. `city-techno-vision/STATUS.md`
3. PR #11 の差分

必要になった関連ファイルだけ追加で読む。
リポジトリ全体の再調査はしない。
`CLAUDE_FENCE_TASK.md` は原則読まない。

## 実行

1. fence クラスを持つ公開済み semantic segmentation モデルを1つ選ぶ。
2. 優先条件:
   - 学習済み重みが公開
   - 追加学習なしで試せる
   - Python から比較的簡単に利用可能
   - ライセンス上の利用条件を確認できる
   - CPUでも最低限テスト可能
3. 候補比較を長く行わず、有力な1モデルを選ぶ。
4. その実モデルに合わせて PR #11 の `FenceDetector` を必要最小限修正する。
5. モデル固有の以下を必ず確認してコードへ反映する。
   - input size
   - RGB/BGR
   - normalization / mean / std
   - model output の形式
   - fence class id
   - resize / interpolation
6. 実際の街中写真で推論する。
7. 以下を end-to-end で確認する。
   - fence mask が取得できる
   - `fence_mask.png` が出る
   - fence から bbox が生成される
   - 通常 YOLO detections と merge される
   - bbox付き画像が出る
   - `detections.json` が出る
   - `detections.yaml` が出る
8. 品質が悪い場合、fine-tuning に進む前に preprocessing / threshold / class id / resize / normalization の問題を切り分ける。

## Do not

- `Tk-work` に触れない。
- 音生成を実装しない。
- JSON/YAML schema を変更しない。
- Open Images V7 detector を置き換えない。
- 大規模リファクタリングをしない。
- 複数の大型モデルを大量ダウンロードしない。
- BDD100K 全体をダウンロードしない。
- fine-tuning を始めない。
- PR #11 を main に merge しない。
- 中間確認が不要なら作業を止めない。

## Token / context discipline

- `city-techno-vision` と PR #11 の必要ファイルだけ読む。
- 長い設計説明を書かず、選定→実装→テストまで進む。
- 過去の会話を復元しない。
- 同じテストを無意味に繰り返さない。
- 外部取得がブロックされたら、必要なモデル名・ファイル・URL/ドメインと、どこまで検証できたかを明示して止める。

## Definition of done

以下が実モデルで確認できたら完了:

```text
実写真
→ pretrained segmentation model
→ fence mask
→ fence bbox
→ normal YOLO detections と統合
→ annotated image
→ detections.json
→ detections.yaml
```

## 完了後

短く以下だけ報告する。

```text
Model:
- ...

Changed:
- ...

Verified:
- ...

Blocked:
- ...   # なければ省略

Next:
- ...
```

作業結果に応じて `STATUS.md` を更新する。
次のタスクへ進む必要がある場合は、`TASK.md` を勝手に別テーマへ書き換えず、次の候補を報告する。
