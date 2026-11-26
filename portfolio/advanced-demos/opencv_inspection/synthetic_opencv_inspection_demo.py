#!/usr/bin/env python3
"""Reproducible OpenCV demo: synthetic shape segmentation and classification.

This is an educational classical-computer-vision baseline, not an AI model
or a production/customer-data result.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np


def make_synthetic_scene(seed: int = 7) -> tuple[np.ndarray, list[dict[str, Any]]]:
    """Return a noisy synthetic BGR image and ground-truth object metadata."""
    rng = np.random.default_rng(seed)
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    image[:] = (28, 32, 38)
    truth: list[dict[str, Any]] = []

    objects = [
        ("circle", (135, 130), 43),
        ("circle", (465, 335), 31),
    ]
    for index, (kind, center, radius) in enumerate(objects, start=1):
        cv2.circle(image, center, radius, (25, 205, 240), thickness=-1)
        truth.append({"object_id": index, "class": kind, "center_x": center[0],
                      "center_y": center[1], "nominal_size": radius})

    rectangles = [
        ((285, 115), (385, 205)),
        ((110, 310), (215, 390)),
    ]
    for index, (top_left, bottom_right) in enumerate(rectangles, start=3):
        cv2.rectangle(image, top_left, bottom_right, (25, 205, 240), thickness=-1)
        truth.append({"object_id": index, "class": "rectangle",
                      "center_x": (top_left[0] + bottom_right[0]) // 2,
                      "center_y": (top_left[1] + bottom_right[1]) // 2,
                      "nominal_size": None})

    noise = rng.normal(0.0, 5.0, image.shape).astype(np.int16)
    image = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    image = cv2.GaussianBlur(image, (5, 5), 0.8)
    return image, truth


def segment_and_classify(image: np.ndarray) -> tuple[np.ndarray, list[dict[str, Any]], np.ndarray]:
    """HSV segmentation + morphology + contour geometry classification."""
    if image is None or image.size == 0 or image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("Expected a non-empty 3-channel BGR image")

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([15, 85, 80], dtype=np.uint8)
    upper = np.array([45, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower, upper)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detections: list[dict[str, Any]] = []
    for contour in contours:
        area = float(cv2.contourArea(contour))
        if area < 500.0:
            continue
        perimeter = float(cv2.arcLength(contour, True))
        if perimeter <= 0:
            continue
        circularity = float(4.0 * np.pi * area / (perimeter * perimeter))
        x, y, width, height = cv2.boundingRect(contour)
        aspect = float(width / height) if height else 0.0
        rectangularity = float(area / (width * height)) if width and height else 0.0
        label = "rectangle" if rectangularity >= 0.90 else "circle"
        detections.append({
            "class": label, "area_px": round(area, 2),
            "circularity": round(circularity, 4),
            "aspect_ratio": round(aspect, 4), "rectangularity": round(rectangularity, 4),
            "x": int(x), "y": int(y), "width": int(width), "height": int(height),
            "center_x": int(x + width / 2), "center_y": int(y + height / 2),
        })
    detections.sort(key=lambda item: (item["center_y"], item["center_x"]))

    annotated = image.copy()
    for index, item in enumerate(detections, start=1):
        x, y, width, height = item["x"], item["y"], item["width"], item["height"]
        cv2.rectangle(annotated, (x, y), (x + width, y + height), (40, 240, 60), 2)
        cv2.putText(annotated, f'{index}: {item["class"]}', (x, max(20, y - 7)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (40, 240, 60), 2, cv2.LINE_AA)
    return mask, detections, annotated


def run(output_dir: Path, seed: int = 7) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    image, truth = make_synthetic_scene(seed)
    mask, detections, annotated = segment_and_classify(image)

    truth_counts = {kind: sum(row["class"] == kind for row in truth)
                    for kind in ("circle", "rectangle")}
    predicted_counts = {kind: sum(row["class"] == kind for row in detections)
                        for kind in ("circle", "rectangle")}
    summary: dict[str, Any] = {
        "status": "SYNTHETIC_BASELINE_ONLY",
        "method": "HSV threshold + morphology + contour geometry",
        "seed": seed,
        "ground_truth_count": len(truth),
        "detected_count": len(detections),
        "ground_truth_by_class": truth_counts,
        "detected_by_class": predicted_counts,
        "count_match": len(truth) == len(detections),
        "class_count_match": truth_counts == predicted_counts,
        "limitations": [
            "Synthetic colored geometric objects only.",
            "No trained AI/deep-learning model.",
            "No customer images, field data, or production acceptance.",
            "Thresholds require recalibration for real illumination, colors, occlusion and camera settings.",
        ],
    }

    outputs = {
        "synthetic_scene.png": image,
        "segmentation_mask.png": mask,
        "detections_annotated.png": annotated,
    }
    for name, array in outputs.items():
        path = output_dir / name
        if not cv2.imwrite(str(path), array):
            raise OSError(f"Could not write output: {path}")

    with (output_dir / "detections.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        fields = ["class", "area_px", "circularity", "aspect_ratio", "rectangularity", "x", "y",
                  "width", "height", "center_x", "center_y"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(detections)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("opencv_demo_output"))
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    summary = run(args.output, args.seed)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["count_match"] and summary["class_count_match"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
