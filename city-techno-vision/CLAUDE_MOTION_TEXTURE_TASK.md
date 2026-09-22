# Claude Task — Motion Texture MVP

## Objective

`city-techno-vision/experiments/visual/motion_texture/` に、
短い街動画を「時間・移動・奥行きを1枚に圧縮した静止画」へ変換するMVPを実装する。

最初に以下だけを読むこと。

1. `city-techno-vision/experiments/visual/motion_texture/README.md`
2. `city-techno-vision/experiments/visual/README.md`
3. `city-techno-vision/.gitignore`
4. 必要になった場合のみ `city-techno-vision/README.md`

**リポジトリ全体を漫然と読み込まないこと。トークン消費を抑える。**

## Constraints

- `Tk-work` には絶対に触れない
- 既存の `detect.py`, `src/`, `tests/` は、MVPに必須でない限り変更しない
- 既存の画像認識パイプラインへ機能を混ぜ込まず、experiments配下に隔離する
- 大きな動画、抽出フレーム、生成物をコミットしない
- MVPでは大型AIモデルを追加しない
- OpenCV / NumPy を中心に、依存追加を最小限にする
- まず静止画1枚を確実に生成することを優先する
- 不要な抽象化、フレームワーク化、全面リファクタをしない

## Implementation target

最低限、以下を作る。

```text
city-techno-vision/experiments/visual/motion_texture/
  README.md
  render.py
  motion_texture.py
  tests/
    test_motion_texture.py
```

CLI例:

```bash
python experiments/visual/motion_texture/render.py \
  --video /path/to/input.mp4 \
  --output-dir experiments/visual/motion_texture/output/
```

想定オプション:

- `--frames`
- `--horizon-y`
- `--strength`
- `--direction`
- `--seed`

## Algorithm

まずはシンプルな temporal displacement composite を実装する。

1. 動画を一定間隔でNフレームにサンプリング
2. 各フレームを同一サイズへ揃える
3. `horizon_y` を基準に縦方向の depth proxy を作る
   - horizon付近: far
   - 画面下端へ近づくほど: near
4. フレーム時刻に応じた変位を与える
5. nearほど変位を大きくし、farほど小さくする
6. フレームを時系列に合成して1枚の画像へする
7. PNG と metadata JSON を出力する

結果は「平均画像」にならないこと。
近景に強い軌跡・引き伸ばしが出て、遠景が比較的残る方向を狙う。

最初の実装はCPUで動けばよい。
処理を理解しやすい小さな関数へ分ける。

## Tests

実動画をテストfixtureとしてコミットしない。

NumPyで作る小さな疑似フレーム、または一時的な小動画を使って最低限以下を検証する。

- frame sampling
- depth proxy
- deterministic output with seed
- output image size
- metadata JSON creation
- invalid input error

実装後、既存テストも実行し、今回の変更で壊していないことを確認する。

## Deliverable

作業が終わったら以下だけを報告する。

1. 変更ファイル
2. 実装したアルゴリズムの要約
3. 実行コマンド
4. テスト結果
5. 実際の短い街動画で試す際に調整すべき3つ以内のパラメータ
6. MVPの見た目を確認してから次に試す改善案（最大3つ）

Motion Texture が完成するまでは Object Echo Windows の実装を開始しない。
