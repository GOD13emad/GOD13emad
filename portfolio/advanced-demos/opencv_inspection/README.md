# OpenCV image-inspection baseline — synthetic portfolio sample

**Status:** local reproducible demonstration; not a client delivery or trained AI model.

## Scope
A small classical-computer-vision pipeline that:
1. Generates a deterministic synthetic scene with two circles and two rectangles.
2. Adds controlled image noise and blur.
3. Segments the colored objects in HSV space.
4. Applies opening/closing morphology.
5. Detects external contours and estimates class using contour area, circularity, bounding-box aspect ratio and rectangularity (contour area / bounding-box area). On the controlled synthetic scene, rectangularity ≥ 0.90 labels a rectangle; otherwise the shape is labelled a circle.
6. Exports an annotated image, segmentation mask, detection CSV and JSON report.

## Run
```powershell
python -m pip install numpy opencv-python-headless pytest
python synthetic_opencv_inspection_demo.py --output .\opencv_demo_output
python -m pytest -q test_synthetic_opencv_inspection_demo.py
```

## Acceptance checks
- Four synthetic objects detected.
- Two circles and two rectangles counted.
- Output images, CSV and JSON are produced.
- Invalid image input fails closed.
- Fixed random seed makes the synthetic scene reproducible.

## Limits and commercial boundary
The sample uses only synthetic colored geometric shapes and classical OpenCV. It does not use a pretrained model, PyTorch, TensorFlow or customer data. The reported class/count agreement applies only to the generated scene. Real imagery requires authorized samples, annotation/ground truth, image acquisition details, train/test separation where learning is used, and buyer-approved metrics (e.g. precision/recall, mAP, IoU, latency). No production accuracy or delivery estimate is inferred.
