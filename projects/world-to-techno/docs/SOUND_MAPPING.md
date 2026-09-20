# Sound Mapping

音の変換ルールはこのプロジェクトの中心資産。

## 初期ルール

| Source | Role | Sound idea | Why |
|---|---|---|---|
| car | bass | low pulse / engine-like bass | 重さ・移動・低域 |
| truck | sub_bass | heavy low hit | 大きさ・重量 |
| bicycle | high_percussion | bell / click | ベル・軽さ |
| person | rhythm | clap / vocal chop | 身体・歩行 |
| construction | industrial_percussion | metallic hit / noise | 機械・打撃 |
| train | sequence | repeating metallic rhythm | 規則的な移動 |
| railroad_crossing | high_percussion | repeated bell | 元々反復音を持つ |
| ambulance | lead | siren-like synth | 強い音程変化 |
| police_car | lead | siren-like synth | 強い音程変化 |
| water | texture | flowing noise | 流動 |
| river | texture | flowing noise | 流動 |
| temple | accent | bell / resonant hit | 鐘・残響 |
| sky | visual_space | ambient / VJ space | 情報量の少ない余白 |
| building | pad | sustained tone | 背景・構造 |
| traffic_light | clock | tick / pulse | 周期・切替 |
| food | sample | material-specific | 食材ごとの差 |
| hamburger | stack | layered loop | 層構造 |
| festival | polyrhythm | hand percussion / chant | 集団反復 |

## 強さ

初期案:

```
intensity =
  confidence * 0.55
+ screen_area * 0.30
+ motion * 0.15
```

値がない項目は既定値を使う。

## まだ決めないこと

音階、キー、具体的なサンプル、BPMの決め方は固定しすぎない。

「視覚要素→音楽的役割」のルールと
「実際にどんな音を鳴らすか」は分離する。

