# Pipeline

## Target pipeline

```
1. Capture
   iPhone等で動画撮影

2. Detect
   フレームごとに物体・場面を検出

3. Track
   同じ対象をフレーム間で追跡

4. Describe
   label / confidence / position / size / motion / duration に変換

5. Map
   対象を音楽上の役割へ変換

6. Arrange
   BPM / density / repetition / mute / gain / transition を決める

7. Render Audio
   実際の音源・サンプル・シンセへ変換

8. Render Visual
   認識枠、ラベル、VJ、演出を映像へ重ねる

9. Sync
   映像と音を同期

10. Export
   TikTok / Reels / YouTube等へ書き出し
```

## v0.1 data contract

入力:

```json
[
  {
    "label": "car",
    "confidence": 0.93,
    "screen_area": 0.24,
    "motion": 0.7
  }
]
```

最低限:
- label
- confidence

任意:
- screen_area: 0.0〜1.0
- motion: 0.0〜1.0

出力:

```json
{
  "bpm": 132,
  "layers": [
    {
      "source": "car",
      "role": "bass",
      "intensity": 0.81,
      "pattern": "steady"
    }
  ]
}
```

## 将来の入力候補

- bounding box
- object count
- color
- luminance
- optical flow
- speed
- direction
- OCR text
- scene category
- GPS / place name
- time of day
- recorded environmental audio

## 技術候補

v0.1はPython標準ライブラリのみ。

将来:
- OpenCV
- YOLO系物体検出
- tracking model
- ffmpeg
- MIDI / Ableton / Logic / custom synth
- Web Audio API
- Core ML / Vision（iPhone内処理する場合）

