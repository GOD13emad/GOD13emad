# Original Computational Verification Demos | نمونه‌های محاسباتی مستقل

**Status: scripts executed and assertions passed on owner Windows host (29 October 2026).** These are original independent *synthetic* demonstrations created to make the numerical methods inspectable; they are not client deliverables or experimental validation.

## 1. Nine-channel Frequency Domain Decomposition (FDD)

Source: [nine_channel_fdd_demo.py](nine_channel_fdd_demo.py).

| Check | Observed result |
|---|---|
| Python libraries | NumPy, SciPy |
| Sensor records | 9 synthetic accelerometer-like channels × 32,768 samples |
| Sampling frequency | 256 Hz |
| Cross-spectrum | Welch, Hann, 8,192-sample window, 4,096 overlap |
| Generated modal resonance centres | 5.00, 11.00, 19.00 Hz |
| Dominant frequencies from FDD singular values | **5.00, 11.00, 18.75 Hz** |
| Maximum absolute peak-frequency error | **0.25 Hz** |
| Minimum modal assurance criterion (MAC) vs synthetic input shapes | **0.999578** |
| Spectral Hermitian residual | 2.48e-17 |
| Test result | `SYNTHETIC_FDD_9CH_PASS` |

The demo synthesizes **independently excited, damped modal response**, projects it to nine virtual sensors, computes the entire 9×9 **complex cross-spectral density**, performs frequency-by-frequency eigen/SVD-equivalent decomposition, selects three spectral peaks without querying the hidden generated resonances, and compares estimated frequencies and shapes **only after** identification.

**Limits:** The input is randomized *simulation*, **not a physical field measurement**; the algorithm does not uniquely reconstruct full physical M/C/K matrices, prove experimental damping, or establish real modal mass calibration. The 19 Hz peak exhibits **0.25 Hz bias**; no zero-error claim.

## 2. State-feedback LQR for mechanical vibration suppression

Source: [lqr_vibration_robustness_demo.py](lqr_vibration_robustness_demo.py).

| Check | Observed result |
|---|---|
| Plant | Linear 1-DOF mass–spring–damper, m=10 kg, c=12 Ns/m, k=150 N/m |
| Disturbance | 100 N, 0.25-second force pulse |
| Control | Continuous-time LQR (algebraic Riccati equation) |
| Uncontrolled peak displacement | **497.066 mm** |
| Controlled peak displacement | **36.296 mm** |
| Peak-displacement reduction in this synthetic test | **92.698%** |
| Peak controller effort | **113.620 N** |
| Robustness grid | **27** mass/damping/stiffness configurations, all closed-loop eigenvalues stable |
| Worst closed-loop eigenvalue real part | **−10.1908 1/s** |
| Test result | `SYNTHETIC_LQR_ROBUST_GRID_PASS` |

The robustness test varies m∈{8,10,12} kg, c∈{8,12,18} Ns/m and k∈{120,150,180} N/m, holding the nominal LQR gain unchanged and checking eigenvalue stability for every combination.

**Limits:** These are synthetic linear plant results; the absolute displacement is deliberately large due to the soft illustrative spring. No physical actuator, saturation, measurement noise, delay, discrete controller, hardware-in-the-loop or laboratory test was performed. The result is **not** a guaranteed improvement on a different plant.

## Running the examples

```shell
python -m pip install numpy scipy
python nine_channel_fdd_demo.py
python lqr_vibration_robustness_demo.py
```

Both scripts use fixed RNG seed / fixed parameter grids, print machine-readable JSON with explicit `scope`, limits and `pass_checks`, and return a nonzero process status if the assertions fail. Exact original host-side source checksums at acceptance:

- FDD: `5014BED77DAB2CCB4C8BAAB47770C989C985BCA1524E33AAC37E01A6179ED9B4`
- LQR: `E5EF340D05072702EFF2C7A61467CE841CAAEBE5E30F3ADE9CD630177C468AC8`

## یادداشت فارسی

این دو تمرین **کد اصلی، قابل‌تکرار و با آزمون اجراشده** هستند. اولی تجزیهٔ دامنهٔ فرکانس (FDD) دادهٔ مصنوعی ۹ کاناله و استخراج فرکانس و شکل مود را آزمایش می‌کند؛ دومی طراحی کنترل‌کنندهٔ بهینهٔ LQR و پایداری در ۲۷ حالت عدم‌قطعیت پارامترهای مکانیکی را می‌سنجد. هیچ‌یک جای دادهٔ واقعی کارفرما، صحت‌سنجی آزمایشگاهی یا پذیرش صنعتی را نمی‌گیرد.
