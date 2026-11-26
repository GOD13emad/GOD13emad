from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import pytest

from synthetic_opencv_inspection_demo import (
    make_synthetic_scene,
    run,
    segment_and_classify,
)


def test_synthetic_scene_is_deterministic():
    first, truth_first = make_synthetic_scene(seed=19)
    second, truth_second = make_synthetic_scene(seed=19)
    assert np.array_equal(first, second)
    assert truth_first == truth_second
    assert len(truth_first) == 4


def test_segmentation_detects_expected_class_counts():
    image, truth = make_synthetic_scene()
    mask, detections, annotated = segment_and_classify(image)
    assert mask.shape == image.shape[:2]
    assert annotated.shape == image.shape
    assert len(detections) == len(truth) == 4
    assert sum(row["class"] == "circle" for row in detections) == 2
    assert sum(row["class"] == "rectangle" for row in detections) == 2
    assert all(row["area_px"] > 500 for row in detections)


@pytest.mark.parametrize("seed", range(32))
def test_each_synthetic_object_matches_ground_truth(seed):
    """Check unique object-level correspondence, not just class totals."""
    image, truth = make_synthetic_scene(seed=seed)
    _, detections, _ = segment_and_classify(image)
    assert len(detections) == len(truth) == 4
    matched = set()
    for expected in truth:
        nearby = [
            index for index, actual in enumerate(detections)
            if (actual["center_x"] - expected["center_x"]) ** 2
            + (actual["center_y"] - expected["center_y"]) ** 2 <= 3 ** 2
        ]
        assert len(nearby) == 1, (seed, expected, nearby)
        index = nearby[0]
        assert index not in matched, (seed, expected, index)
        assert detections[index]["class"] == expected["class"], (seed, expected)
        matched.add(index)
    assert matched == set(range(len(detections)))


def test_run_writes_reconciled_outputs(tmp_path: Path):
    summary = run(tmp_path)
    assert summary["status"] == "SYNTHETIC_BASELINE_ONLY"
    assert summary["count_match"] is True
    assert summary["class_count_match"] is True
    for name in (
        "synthetic_scene.png", "segmentation_mask.png",
        "detections_annotated.png", "detections.csv", "summary.json",
    ):
        assert (tmp_path / name).is_file()
        assert (tmp_path / name).stat().st_size > 0
    loaded = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    with (tmp_path / "detections.csv").open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert loaded == summary
    assert len(rows) == 4


def test_invalid_image_fails_closed():
    with pytest.raises(ValueError):
        segment_and_classify(np.zeros((0, 0, 3), dtype=np.uint8))
