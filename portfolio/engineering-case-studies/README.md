# Engineering & Research Case Studies — Evidence-bound Portfolio
# پروژه‌های مهندسی و پژوهشی — با تفکیک دستاورد و محدودیت

This index describes genuine engineering workflows with inspected project files or official project-status documents. Some artifacts are private or belong to ongoing research; **their full source files and project-specific materials are not uploaded here**. Recorded numerical results are tied to the stated study/revision, **not** a claimed production-validated system.

## 01 — Electromechanical generator concept: CAD, 2D electromagnetics and manufacture-ready drawings

**Scope:** 750 W *design-point* permanent-magnet generator development; a historical 12-pole/36-slot, 500 rpm, three-phase configuration in an extended electromagnetic-engineering project. The engineering workspace contains COMSOL and SolidWorks work, winding configuration studies, design controls and review artifacts.

**Physical artifacts verified on the owner's workstation (29 October 2026):**

- **21 native SolidWorks drawings** (`.SLDDRW`) and their **21 matching PDF drawings** in the R27 manufacturing drawing package. Example drawing subjects include overall assembly, stator, rotor stack, shaft/key, magnets and end caps.
- Local project documentation records a 2D electromagnetic power study and iterative SolidWorks assembly/interference work. Historical 2D simulations include an approximately **743.75 W** study result for the 500 rpm design point; **computed, not measured output**, and not independent proof of final 3D electromagnetic or prototype performance.
- Modeling, drawing and simulation evidence are separate from procurement, physical build, durability, thermal acceptance or validated generator power tests.

**Status:** digital model and manufacturing-drawing research evidence available; full 3D solution, prototype and independent physical acceptance remain open. The larger alternative electromagnetic motion research is **not** a perpetual-motion or free-energy result.

**What this demonstrates:** CAD-to-analysis-to-drawing workflow, machine element detailing, multiphysics simulation, design traceability, dimensional verification and honest acceptance criteria.

## 02 — Native SOLIDWORKS automation and engineering CAD productization

**Scope:** building a parametric, native-CAD automation/workstation pipeline to turn input parameters, engineering geometry and structured modeling plans into SOLIDWORKS parts/assemblies/drawings, preserving dependency identity and verification evidence.

**Evidence:** Local canonical project `GENERAL_CAD_WORKSTATION_BUILDER` has accepted production assembly CAD, native drawing package, verified file hashes, interference audit and a separate installed release candidate. The authoritative October control record states:

- `WholeAssemblyInterferenceAuditStatus = PASS_ZERO_POST_INSERTION` with **zero positive interference** in the accepted inspected assembly.
- `NativeDrawingPackageAccepted = true`.
- `InstalledReceiptExactHashVerified = 266` and `InstalledReceiptFileIssues = 0` for the scope of the recorded consolidation.
- Candidate installer **1.0.0-rc.18**, with **FinalReleaseReady = false** and the external unseen-validation gate not passed.
- Model/feature compiler and tests cover source-bounded geometry, parametric design, SOLIDWORKS native readback, regression and recoverable actions.

**Status:** accepted scoped native-CAD evidence and release-candidate tooling, **not** fully accepted general-purpose CAD software or universally solved drawing-to-solid inference. Private source and customer-specific models are not published.

## 03 — Nine-channel operational modal analysis: FDD/EFDD/SSI and modal-mass identifiability

**Scope:** system identification for cantilever beams with multiple response sensors, broadband/random excitation, mass-loading studies, FDD/EFDD/SSI, correlation to ARTeMIS and complex FE/ANSYS test cases.

The research workspace contains a separate documented code catalog with more than 1,100 source files (including **929 Python, 83 MATLAB, 62 PowerShell, 19 ANSYS input** files in a snapshot), and notes substantial vibration, sensor-spectrum, finite-element and result-validation workflows. Source counts indicate **research scope**, not that every file is a mature product.

The R444 research report explicitly records **24 independently generated synthetic 9-channel time-series files**, each containing **76,800 samples per channel**, and **41** mass-condition equations, with independent spectral/Welch consistency checks. A simple dual spatial projection passed **one** hold-one-condition mass test at **9.758%** error, but failed the RMS and hold-one-station conditions. **The unique physical 9×9 M/C/K matrices have not been identified from field measurements, and external ARTeMIS validation was not completed.**

**Original, publicly reproducible related sample:** [9-channel synthetic FDD with actual Python runtime assertions](../advanced-demos/README.md).

**Status:** substantial methodological and synthetic QA work; major scientific inference/field-data gates deliberately remain open.

## 04 — Electromagnetic rotor/magnet dynamics and energy-accounting research

**Scope:** multiple COMSOL 2D/3D electromagnetic motion and torque studies with 16+5-magnet geometric variants, moving meshes, Maxwell torque, and energy accounting.

The project's documented current status (October 2026) includes a native 3D G10 one-angle mesh/solution for a **21-magnet** configuration, a **local** six-mesh torque cross-check with approximately **1.015%** difference vs the re-meshed reference, and a **curved-element minimum mesh quality 0.02213** below the project's 0.1 warning criterion. The general time-dependent torque, mechanical motion and **all energy-port accounting** remain unresolved.

**Status:** computational research and local checks only. **No continuous autonomous energy output, energy gain, self-sustaining machine, physically validated commercial generator or proven free-energy claim.** This project's rigorous evidence holds are part of its scientific evaluation, not a defect to hide.

## 05 — COMSOL independent runtime acceptance: heat transfer and fluid mechanics

Two vendor-supplied COMSOL Multiphysics 6.4 example models were actually executed on the user's Windows system on 29 October 2026, with original model files kept untouched:

| Official reference case | Numerical evidence | Outcome |
|---|---|---|
| `heat_radiation_1d.mph` | stationary nonlinear heat transfer, 31 DOF plus internal variables | **100% solved**, exit 0, saved output |
| `blasius_boundary_layer.mph` | stationary nonlinear fluid boundary layer, 70,377 DOF | **100% solved**, exit 0, saved output |

The results demonstrate **an operational installation and convergence on these two vendor examples**, not novel client-specific simulations, software vendor certification, model-independent validation, or a COMSOL commercial license. Owner-specific commercial-use licensing remains to be verified before a paid COMSOL project.

## 06 — Controlled engineering computation and model verification

Cross-disciplinary engineering workflow implemented across projects: source-file attribution and hashing, unit consistency, baseline vs candidate comparisons, explicit physical constraints, independent numerical recalculations, geometry/mesh/solver checks and handoffs with clearly marked unpassed gates.

Three **new original, tested** compact public scripts extend this portfolio: [nine-channel FDD](../advanced-demos/nine_channel_fdd_demo.py) and [robust LQR state feedback with a 27-case parameter sweep](../advanced-demos/lqr_vibration_robustness_demo.py), plus [robust two-DOF TMD frequency-response optimization](../advanced-demos/robust_2dof_tmd_demo.py). A separate [three-member truss MATLAB optimization](../matlab-three-bar-truss/README.md) is also available.

---

## گزیدهٔ فارسی

این پرونده صرفاً شامل یک مثال آموزشی نیست، بلکه دامنه‌ای از **طراحی ژنراتور مغناطیس دائم، مدل‌سازی الکترومغناطیسی، نقشه‌های بومی SolidWorks، اتوماسیون CAD، تحلیل دینامیک و ارتعاشات، شناسایی مودال ۹کاناله و اعتبارسنجی عددی در COMSOL و MATLAB/Python** را پوشش می‌دهد. دستاوردهای محدود به مدل، کد، نقشه، مطالعهٔ مصنوعی و محاسبات عددی به‌طور روشن از **آزمون آزمایشگاهی، نصب تجاری و پذیرش محصول نهایی** جدا شده‌اند.

بخشی از مدارک فنی پروژه‌ها خصوصی، پژوهشی یا دارای وابستگی قراردادی‌اند؛ برای جلوگیری از انتشار بدون بررسی حقوق دسترسی، در این مخزن تنها **خلاصهٔ قابل ارائه و مستند** آمده است. فایل‌های اصلی هر پروژه فقط در چارچوب مجوز، محرمانگی و توافق همان پروژه قابل بررسی هستند.
