# Object Echo Windows — Future MVP

Motion Texture の次に試す視覚表現。

## Concept

動画内で認識した対象を bbox で切り出し、小さなウィンドウとして画面内に残す。
対象の移動に追従しながら、過去の切り出しが残像のように増殖していく。

例:

- 人 → 顔や身体の小窓が時系列で残る
- 車 → 走行軌跡に沿って車の小窓が残る
- 看板 → 切り出された看板が画面内に漂う
- fence → 部分画像を分割・反復する

## Reuse existing data

既存の detection JSON の以下を使える形を優先する。

- frame id / timestamp（動画対応時に追加）
- label
- group
- confidence
- minx / maxx / miny / maxy

## Scope

この実験は Motion Texture MVP が一度完成してから着手する。
現時点では設計メモのみで、実装は始めない。
