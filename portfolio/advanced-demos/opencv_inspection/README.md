# OpenCV image-inspection baseline — synthetic portfolio sample

**Status:** local reproducible demonstration; not a client delivery or trained AI model.

## Scope
A small classical-computer-vision pipeline that:
1. Generates a deterministic synthetic scene with two circles and two rectangles.
2. Adds controlled image noise and blur.
3. Segments the colored objects in HSV space.
4. Applies opening/closing morphology.
5. Detects external contours, rejects those below 500 px² or with nonpositive perimeter, and records area, circularity, bounding-box aspect ratio and rectangularity (contour area / bounding-box area). The class decision uses rectangularity alone: ≥ 0.90 labels a rectangle; otherwise the shape is labelled a circle. This is a closed two-class rule for the synthetic scene, not a general circle detector.
6. Exports an annotated image, segmentation mask, detection CSV and JSON report.

## Run
```powershell
python -m pip install "numpy>=1.24,<3" "opencv-python-headless>=4.10,<5" "pytest>=8,<9"
python synthetic_opencv_inspection_demo.py --output .\opencv_demo_output
python -m pytest -q test_synthetic_opencv_inspection_demo.py
```

## Acceptance checks
- Four synthetic objects detected.
- Two circles and two rectangles counted.
- Output images, CSV and JSON are produced.
- Invalid image input fails closed.
- Fixed random seed makes the synthetic scene reproducible within a given software environment. The dependency ranges match CI but are not a fully locked environment; bitwise reproducibility across versions is not asserted.

## Limits and commercial boundary
The sample uses only synthetic colored geometric shapes and classical OpenCV. It does not use a pretrained model, PyTorch, TensorFlow or customer data. The reported class/count agreement applies only to the generated scene and does not by itself establish per-object matching or precision/recall. Real imagery requires authorized samples, annotation/ground truth, image acquisition details, train/test separation where learning is used, and buyer-approved metrics (e.g. precision/recall, mAP, IoU, latency). No production accuracy or delivery estimate is inferred.
