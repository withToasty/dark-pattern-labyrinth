# Visual Experiments

City Techno Vision の視覚表現を試すための実験区画。

本体の画像認識パイプラインを壊さず、まず小さなMVPとして検証する。
実験が有効だと判断できたものだけ、後で `src/` 側へ昇格する。

## Roadmap

### 1. Motion Texture
**先に実装する。**

街の短い動画を、時間・移動・奥行きの痕跡を残した1枚の静止画へ圧縮する。

- input: short video
- output: one PNG + parameters/metadata JSON
- goal: 単なる代表フレームや平均画像ではなく、「その場所を通過した時間」が1枚で感じられること
- first MVP: 軽量な OpenCV / NumPy ベース
- later candidates: optical flow / monocular depth / existing horizon data

詳細: [motion_texture/README.md](motion_texture/README.md)

### 2. Object Echo Windows
**Motion Texture の後に試す。**

動画内で検出した人物・車・看板などを bbox で切り出し、小窓として追従・残像・増殖させる表現。

既存の detection JSON（label / group / bbox / confidence）を再利用できる設計を優先する。

詳細: [object_echo_windows/README.md](object_echo_windows/README.md)

## Repository policy

- 大きな動画・抽出フレーム・生成物はGit管理しない
- `Tk-work` には触れない
- 音生成は引き続き別プロジェクトの責務
- 実験コードから既存の検出・ホライゾン機能を壊さない
