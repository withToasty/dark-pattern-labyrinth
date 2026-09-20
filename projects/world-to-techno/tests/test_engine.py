from world_to_techno.engine import build_arrangement


def test_build_arrangement_maps_known_labels_and_tracks_unknowns():
    detections = [
        {"label": "car", "confidence": 0.9, "screen_area": 0.2, "motion": 0.5},
        {"label": "mystery", "confidence": 0.9},
    ]
    sound_map = {
        "car": {"role": "bass", "pattern": "steady"},
    }

    result = build_arrangement(detections, sound_map)

    assert result["layer_count"] == 1
    assert result["layers"][0]["role"] == "bass"
    assert result["unknown_labels"] == ["mystery"]
    assert 124 <= result["bpm"] <= 140
