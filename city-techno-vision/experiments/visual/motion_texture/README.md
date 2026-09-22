# Motion Texture — MVP

## Concept

短い街動画を、**時間・移動・奥行きを1枚に圧縮した静止画**へ変換する。

狙いは「動画の1フレームを選ぶ」ことではない。
手前のものは大きく流れ、奥のものはゆっくり残るような時間差を1枚に積層し、
撮影した場所を通過した体験そのものを静止画として残す。

## MVP goal

5〜15秒程度の動画を入力し、1枚のPNGを生成できること。

最初から正確な3D復元はしない。
まずは軽量なルールベースで「奥行きらしさ」と「時間の蓄積」が見えるかを検証する。

## Usage (実装済み)

`city-techno-vision/` から実行する:

```bash
python experiments/visual/motion_texture/render.py \
  --video path/to/input.mp4 \
  --output-dir experiments/visual/motion_texture/output/ \
  --frames 12 \
  --horizon-y 0.55 \
  --strength 40 \
  --direction auto \
  --seed 0
```

出力 (`--output-dir` 配下、Git管理外):

- `<name>_motion_texture.png` — 合成された静止画
- `<name>_motion_texture.json` — 使用したパラメータのメタデータ

パラメータ:

- `--frames` (int, default 12): サンプリングするフレーム数（最低2）
- `--horizon-y` (float, default 0.55): 0〜1の正規化値。この行より上を「奥」、下を「手前」とみなす
- `--strength` (float, default 40.0): 手前側（画面下端）の最大変位量（px）
- `--direction` (left / right / auto, default auto): 変位の向き。`auto` は `--seed` から決定的に選ぶ簡易版（光学フロー等の高度な方向推定はMVP範囲外）
- `--seed` (int, default 0): 再現用。`auto` の向きと、フレームごとの変位ジッターに使う

## MVP algorithm

まずは以下のような単純な方法から始める。

1. 動画から一定間隔でフレームをサンプリング
2. 全フレームを同じサイズに正規化
3. horizon より下ほど「手前」とみなす depth proxy を作る
4. 時系列に応じて各フレームを少しずつ変位させる
5. 手前ほど変位量を大きく、奥ほど小さくする
6. 時間順のマスク / ブレンドで1枚へ合成
7. PNG と、使ったパラメータを JSON で保存

見た目としては、色や輪郭が横方向・進行方向へ引き伸ばされ、
遠景は比較的安定し、近景ほど強く時間の軌跡が出る状態を狙う。

## Important constraints

- MVPでは新しい大型AIモデルを必須にしない
- 既存の YOLO / SegFormer / horizon パイプラインに依存しなくても単独実行できること
- 既存コードの大規模リファクタはしない
- `Tk-work` には触れない
- 入力動画・抽出フレーム・出力画像はGitへコミットしない
- 依存追加は最小限にする
- まず「1枚出る」ことを優先し、作品品質の最適化は後段に回す

## Acceptance criteria

- [x] mp4 / mov の短い動画を読める
- [x] 指定数のフレームをサンプリングできる
- [x] depth proxy によって上下で変形量が変わる
- [x] 時系列情報が1枚のPNGに残る
- [x] 同じ入力・seed・パラメータなら再現できる
- [x] パラメータをJSONに保存する
- [x] 失敗時に分かるエラーメッセージを出す
- [x] 既存テストを壊さない
- [x] READMEに実行例とパラメータ説明を残す

## Tests

```bash
cd city-techno-vision
python -m pytest experiments/visual/motion_texture/tests/test_motion_texture.py -v
```

実動画はコミットせず、NumPyの疑似フレームと `cv2.VideoWriter` で作る一時動画（テスト内でのみ生成、破棄）でカバーする。

## Not in MVP

- 正確な3D depth estimation
- optical flow の高度な補正
- object detectionとの統合
- 音生成
- リアルタイム処理
- GUI / Web UI

これらは、MVP画像を見て表現として面白いと判断した後に追加する。

## Next experiment

Motion Texture の次は
[Object Echo Windows](../object_echo_windows/README.md) を試す。
