# MATLAB Structural Optimization — Independent Portfolio Demonstration

> **Independent synthetic study.** This is a small self-authored educational verification exercise, **not** completed client work or a representation of any customer's three steel structures.

## Scope and computational model

- A 2D pin-jointed three-bar steel truss: three fixed support nodes, one free joint with two displacement DOFs.
- Material: linear elastic steel, elastic modulus **210 GPa**, density **7,850 kg/m³**.
- Load at the free node: **+10 kN** horizontal, **−30 kN** vertical.
- Design variables: three bar cross-sectional areas. The objective is minimum member mass subject to displacement, axial stress and area limits.
- Limits: absolute free-joint displacement **≤ 0.12 mm**, axial stress **≤ 120 MPa**, each bar area between **100 and 4,000 mm²**.

## Results — synthetic example only

| Check | MATLAB R2025b verified output |
|---|---:|
| Baseline mass | 36.063784 kg |
| Reduced mass | 13.570482 kg |
| Relative mass reduction | **62.371%** |
| Optimized bar areas | 100.000, 561.196, 793.651 mm² |
| Maximum absolute displacement | 0.120000 mm (0.120000 mm limit) |
| Maximum absolute axial stress | 25.199995 MPa (120 MPa limit) |
| Relative equilibrium residual | 0.000e+00 |

The script executed successfully on **MATLAB R2025b**, with `INDEPENDENT_TOY_DEMO PASS` and process exit code 0. The calculations were also independently re-evaluated with NumPy, with agreement to the printed numerical precision.

The optimization uses the MATLAB base `fminsearch` algorithm with multiple initial seeds and an explicit constraint penalty. The script verifies **feasibility and equilibrium**, **not global optimality** or suitability for an undisclosed real-life geometry. This example does not require the Optimization Toolbox.

## Reproduction

1. Open MATLAB R2025b (earlier compatible releases may work but were not tested).
2. Run `truss_optimization_demo` from this directory.
3. Inspect the printed mass, section areas, displacement, stress and residual, and the built-in assertions.

**Source:** [truss_optimization_demo.m](./truss_optimization_demo.m)

## معرفی فارسی

این نمونه‌کار یک مثال **آموزشی و مستقل با داده‌های فرضی** دربارهٔ بهینه‌سازی جرم خرپای دوبعدی سه‌عضوی در MATLAB است. متغیرهای طراحی، سطح مقطع اعضا هستند و قیود جابه‌جایی، تنش محوری و حدود سطح مقطع به‌صورت صریح بررسی می‌شوند. نتیجهٔ کاهش جرم **۶۲٫۳۷۱ درصد** فقط به همین مدل ساختگی مربوط است.

کد و خروجی آن در MATLAB R2025b اجرا و بررسی شده‌اند. این فایل **پروژهٔ واقعی هیچ کارفرمایی نیست**، بهینهٔ سراسری را اثبات نمی‌کند و جایگزین بررسی هندسه، فایل‌ها و الزامات سفارش‌های مستقل نخواهد بود.
