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

## Proposed interface

```bash
python experiments/visual/motion_texture/render.py \
  --video path/to/input.mp4 \
  --output-dir experiments/visual/motion_texture/output/
```

初期パラメータ候補:

- `--frames`: 使用するサンプルフレーム数
- `--horizon-y`: 0〜1の正規化値。未指定時は安全な既定値
- `--strength`: 手前側の変形量
- `--direction`: left / right / auto
- `--seed`: 再現用

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

- [ ] mp4 / mov の短い動画を読める
- [ ] 指定数のフレームをサンプリングできる
- [ ] depth proxy によって上下で変形量が変わる
- [ ] 時系列情報が1枚のPNGに残る
- [ ] 同じ入力・seed・パラメータなら再現できる
- [ ] パラメータをJSONに保存する
- [ ] 失敗時に分かるエラーメッセージを出す
- [ ] 既存テストを壊さない
- [ ] READMEに実行例とパラメータ説明を残す

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
