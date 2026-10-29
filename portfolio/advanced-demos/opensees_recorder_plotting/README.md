# OpenSees-style Recorder output to SVG — independent numerical aid

**Scope:** An original **post-processing-only** Python 3 program for ordinary whitespace- or comma-delimited numeric Recorder files. **Eight of eight unit tests passed on the author's Windows Python environment on 29 October 2026.**

**This is NOT a run of the OpenSees solver and is NOT any client's model, code, output or paid deliverable.** OpenSees / OpenSeesPy was **not installed** in the owner's checked desktop environment. All test input is fabricated locally.

## How it relates to structural analysis

The OpenSees *Node Recorder* can export a column of analysis time together with a selected degree-of-freedom response. For example, the following is **illustrative Tcl syntax only**; a real model must have an appropriate node and DOF:

```tcl
recorder Node -file node1_disp.out -time -node 1 -dof 1 disp
```

After running a **legitimate, correctly configured** OpenSees simulation, a typical numeric output can be plotted without MATLAB:

```bash
python opensees_recorder_plot_demo.py --input node1_disp.out --output node1_disp.svg --column 1 --title "Node 1 displacement" --ylabel "Displacement (model units)"
```

The tool expects an *explicit* time column (e.g. Recorder configured with `-time`), finite numeric rows, at least two time steps, consistent column counts and strictly increasing time. The first column is time; `--column 1` selects the first response column, `--column 2` the next. It does not infer physical units or validate the accuracy/convergence of the solver.

**Source:** [opensees_recorder_plot_demo.py](opensees_recorder_plot_demo.py)  
**Tests:** [test_opensees_recorder_plot_demo.py](test_opensees_recorder_plot_demo.py)  
**Verify:** `python -m unittest discover -s . -p 'test_opensees_recorder_plot_demo.py' -v`

The SVG is XML with escaped display labels. Input validation rejects inconsistent row shapes, time ordering errors and NaN/Infinity; constant data plots with an automatic visual range. No internet, pip packages, credentials or proprietary MATLAB licence needed for this independent plotting script.

**Boundary:** Actual OpenSees executables, solver installation, Tcl compatibility, source-code rights and response trustworthiness must be verified separately for any client use. For client teaching or project delivery, license compliance and acceptance of a Python plotting alternative must be established in the legitimate contract. Do not claim that these toy tests reproduce an academic paper or customer's geotechnical analysis.

**Primary references:** [official OpenSees Recorder documentation](https://opensees.github.io/OpenSeesDocumentation/user/manual/output/PlotRecorder.html), [Berkeley OpenSees developer license](https://openseesdocumentation.readthedocs.io/en/latest/developer/license.html).
