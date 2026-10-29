# Software Engineering Portfolio — Released Products & Live Systems
# نمونه‌کارهای نرم‌افزاری — محصولات منتشرشده و سامانه‌های درحال توسعه

The following records link to the owner's **actual public repositories**, official release statements and per-project evidence. Development, preview, release-candidate and stable states are distinguished. A GitHub repository is not proof of universal installation acceptance or a public-trust Authenticode certificate.

## 01. [Taskbar Monitor Enhanced](https://github.com/GOD13emad/TaskbarMonitorEnhanced)

**Platform:** Windows desktop | monitoring / sensor isolation / taskbar integration / UI rendering.

- Actual publicly released, versioned **v1.7.9** installer as of 29 Oct 2026, with GitHub release, SHA-256 and an explicit owner-accepted **unsigned** distribution record.
- **49 renderer-backed themes**, with 20 original Studio designs plus theme renderer regressions.
- An **eight-page Performance Workspace** for overview, processes, network, storage, alerts, themes, profiles and hardware, plus nine-page Settings.
- Hardware sampling and sensor-process isolation, per-user installation/upgrade paths, privacy-oriented local retention, CSV/JSON evidence, update handling and an installed application QA workflow.
- Publisher Authenticode on the v1.7.9 public installer is **NotSigned**. Source/CI/provenance do not substitute for a trusted signing key.

**Technical focus:** C#/Windows desktop engineering, UI/UX, instrumentation, data integrity, installer design, regression gates, release provenance.

## 02. [ChatGPT Remote Commander](https://github.com/GOD13emad/ChatGPTRemoteCommander)

**Platform:** Windows/Linux | remotely authorized, bounded machine/project access through MCP.

- Source/release maintainer attribution is recorded publicly in the project's maintainer policy; work is collaborative and not represented as exclusively solitary authorship.
- Tooling for constrained file operations, detached commands, recoverable mutations, browser/UI permission boundaries, multi-machine operation, per-account tunnel enrollment, audit evidence and Windows/Linux service persistence.
- Documentation includes setup guides in **10 languages** and precise platform-specific installer paths.
- As of the October 2026 repository authority, the **0.11 development train has no accepted integrated Stable**. Historical Core artifacts, separate browser components and CI acceptance cannot be presented as a complete fully qualified 1.0.0 product.

**Technical focus:** TypeScript/Node.js, MCP tool development, security boundaries, remote systems administration, execution traceability, cross-platform deployment.

## 03. [FreeNet Hub](https://github.com/GOD13emad/FreeNetHub)

**Platform:** Windows/Linux | network diagnostics and user-controlled connectivity.

- Owner-managed application with Dashboard, Methods, Nodes, Tools and Settings areas and release-specific AUTO, WARP, Tor/bridge, proxy/tunnel and node health workflows.
- Public repo documents versioned Windows and Linux release assets, verified digests, rollback and install/update invariants, native permissions and explicit failure behavior.
- Previous public Windows R53 and Linux R21 releases are distinguished from newer field-test/preview builds.
- Narrow browser-proxy checks **do not** prove whole-device DNS/UDP leak protection, ISP reachability for all hosts, or authenticated third-party account access. Global deployment acceptance is not implied.

**Technical focus:** cross-platform UI, software/network integration, resilient update pipelines, user-consented network lifecycle and nonfabricated diagnostics.

## 04. [Open Internet Gateway](https://github.com/GOD13emad/OpenInternetGateway)

**Platform:** Windows/Linux | separate managed tunnel/relay application and measurement workflows.

- Documented independent physical-adapter baseline measurements, bounded node testing, real tunnel throughput and UI-visible status.
- Versioned update paths with three-way downloaded/release/hash checks, distinct Windows and Linux backend handling and explicit network safety rules.
- App/relay status not conflated with internet freedom guarantees or unrestricted access to third-party sites.

**Technical focus:** Electron desktop front end, platform services, connectivity lifecycle, health/verification tests and self-healing configuration safety.

## 05. [Direct Internet Method](https://github.com/GOD13emad/DirectInternetMethod)

**Platform:** Windows WPF/.NET 10 and Linux protected backend.

- Public project README records **v1.5.4 Stable** with Windows and Linux official packages and SHA-256 evidence (October 2026).
- Targeted DNS/DPI processing and diagnostics, with a clear distinction from a VPN or generic HTTP/SOCKS tunnel.
- Native Windows upgrade/rollback workflows and Linux systemd/PolicyKit/permission boundaries with independent verification records.
- Site transport, regional access policy and authenticated user authorization are separate properties; no claim of bypassing account or sanctions controls.

**Technical focus:** .NET/WPF services, Linux system integration, package/release engineering, diagnostics, bounded state changes.

## 06. [PersianWordAgent](https://github.com/GOD13emad/PersianWordAgent)

**Platform:** Windows x64 and native Microsoft Word automation.

- **Version 1.0.0** published as an owner-distributed binary package under an explicit proprietary binary-distribution license.
- Persian/RTL document classification and controlled-copy repair; Word-native heading/TOC refresh, captions, table/pagination integrity checks and guarded fail-closed operations.
- The application source is **not published** in this release repository. Hash-bearing package provenance is not a statement of public Authenticode trust.

**Technical focus:** Office automation, RTL/Persian typographic handling, document quality assurance, recoverable transformations.

## 07. Mechanical / Scientific Computing Workflows

The owner maintains substantial local engineering computational pipelines beyond the public software repositories, including SOLIDWORKS native geometry automation, model QA, COMSOL multiphysics solver scripts, MATLAB/Simulink and Python vibration/system-identification studies. See [engineering case studies](../engineering-case-studies/README.md).

## 08. Original published numerical algorithm demonstrations

New original source backed by actual execution assertions:

- [9-channel FDD cross-spectrum and modal peak estimation](../advanced-demos/nine_channel_fdd_demo.py)
- [LQR vibration reduction and 27-case robustness grid](../advanced-demos/lqr_vibration_robustness_demo.py)
- [Robust 2DOF tuned mass damper synthesis and 3-case uncertainty sweep](../advanced-demos/robust_2dof_tmd_demo.py)
- [MATLAB mechanical truss constrained mass optimization](../matlab-three-bar-truss/truss_optimization_demo.m)

These are **synthetic models**, not fabricated client success stories. Each source discloses its scope, reproducibility and technical limitations.

---

## شناسنامهٔ فارسی

مجموعهٔ نرم‌افزارهای عمومی این پروفایل شامل **پایش منابع و سخت‌افزار ویندوز، ابزارهای کنترل‌شدهٔ راهبری و اتوماسیون رایانه، سامانه‌های مدیریت اتصال برای ویندوز/لینوکس، نرم‌افزارهای مبتنی بر .NET و ابزار تخصصی ویرایش و کنترل کیفیت اسناد فارسی در Microsoft Word** است.

برای هر پروژه، **لینک مخزن رسمی، وضعیت انتشار، شواهد نسخه و تمایز بین امکانات موجود و قابلیت‌های آزمایش‌نشده** رعایت شده است. پروژه‌های مشترک با نسبت‌دهی درست به مشارکت‌کنندگان معرفی می‌شوند. این صفحه، رزومهٔ حرفه‌ای و فنی است و جایگزین قرارداد، بررسی دسترسی به کد خصوصی، یا تعهد تحویل محصول جدید نمی‌شود.
