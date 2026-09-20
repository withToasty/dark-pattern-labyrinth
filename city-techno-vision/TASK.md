# TASK — PR #11 を merge-ready に整理する

## Goal

fence の実モデル end-to-end 検証は成功済み。
今回は新機能を追加せず、PR #11を安全にレビュー・mergeできる状態へ整理する。

## 最初に読むもの

1. `CLAUDE.md`
2. `city-techno-vision/STATUS.md`
3. この `TASK.md`
4. PR #11 の現在の差分

必要なファイルだけ読む。

## 実行

1. PR #11ブランチ上の一時fixture
   `city-techno-vision/tests/fixtures/kobe_fence_test.jpg`
   を削除する。
2. main の最新変更を PR #11ブランチへ取り込み、現在の `mergeable=false` の原因となる競合を解消する。
3. `CLAUDE.md` / `STATUS.md` / `TASK.md` の運用を壊さない。
4. fence実装に関係する既存テストを再実行する。
5. 通常 detector の既存経路を壊していないことを確認する。
6. PR #11がmergeableになったか確認する。
7. 不要な一時ファイルが残っていないことを確認する。

## Do not

- PR #11をmainへmergeしない
- fenceモデルを変更しない
- threshold調整を始めない
- fine-tuningを始めない
- 別モデル比較を始めない
- 音生成へ進まない
- `Tk-work` に触れない
- 大規模リファクタリングをしない
- 実モデル検証が成功したコードを理由なく作り直さない

## 検証済み事実

GitHub Actions run `35527951489` で実写真 end-to-end 検証済み。

- total detections: 6
- fence detections: 2
- `fence_mask.png` 生成成功
- annotated image 生成成功
- JSON/YAML 生成成功
- artifact upload 成功

この検証をやり直す必要はない。
競合解消によって fence関連コードを実質変更した場合のみ再検証の必要性を報告する。

## Definition of done

- 一時fixture削除
- mainとの競合解消
- tests pass
- PR #11 が mergeable
- PR #11 はまだ open / unmerged

## 完了後

```text
Changed:
- ...

Verified:
- ...

PR:
- mergeable: yes/no
- merged: no

Next:
- ...
```
