#!/usr/bin/env python3
"""Independent, offline OpenSees-style numeric Recorder-to-SVG helper.

No OpenSees runtime, third-party packages, private model or commercial MATLAB.
Use only on the client's lawful, permitted output files after explicit engagement.
"""
from __future__ import annotations

import argparse
import html
import math
from pathlib import Path

PALETTE = ("#145DA0", "#D96C00", "#2E7D32", "#762EA5")


def read_recorder(path: Path) -> list[tuple[float, ...]]:
    """Read whitespace/comma-separated, strictly increasing time + 1..N values.

    Requires explicit '-time' for the first column in a real OpenSees Recorder.
    Ignores '#' comment and blank lines; rejects incomplete or invalid records.
    """
    records: list[tuple[float, ...]] = []
    width = None
    with Path(path).open("r", encoding="utf-8-sig") as f:
        for n, text in enumerate(f, 1):
            line = text.split("#", 1)[0].strip()
            if not line:
                continue
            try:
                values = tuple(float(item) for item in line.replace(",", " ").split())
            except ValueError as err:
                raise ValueError(f"line {n}: not a numeric recorder row") from err
            if len(values) < 2 or (width is not None and len(values) != width):
                raise ValueError(f"line {n}: inconsistent number of output columns")
            if any(not math.isfinite(v) for v in values):
                raise ValueError(f"line {n}: nonfinite result")
            if records and values[0] <= records[-1][0]:
                raise ValueError(f"line {n}: time must strictly increase")
            width = len(values)
            records.append(values)
    if len(records) < 2:
        raise ValueError("need at least two numeric time steps")
    return records


def svg_chart(records: list[tuple[float, ...]], *, title: str = "Synthetic Recorder",
              ylabel: str = "Response (model units)", channel: int = 1) -> str:
    if not records or not (1 <= channel < len(records[0])):
        raise ValueError("channel must be an existing 1-based response column")
    if len(records) < 2 or any(len(r) != len(records[0]) for r in records):
        raise ValueError("invalid recorder geometry")
    x = [r[0] for r in records]
    y = [r[channel] for r in records]
    if any(not math.isfinite(v) for v in (*x, *y)):
        raise ValueError("nonfinite input")
    if any(x[i] <= x[i-1] for i in range(1, len(x))):
        raise ValueError("time must strictly increase")
    ymin, ymax = min(y), max(y)
    if ymin == ymax:
        pad = 1.0 if ymin == 0 else abs(ymin) * 0.05
        ymin -= pad
        ymax += pad
    width, height, left, right, top, bottom = 780, 440, 95, 30, 65, 75
    plot_w, plot_h = width-left-right, height-top-bottom
    X = lambda v: left + (v-x[0])/(x[-1]-x[0])*plot_w
    Y = lambda v: top + (ymax-v)/(ymax-ymin)*plot_h
    points = " ".join(f"{X(xv):.2f},{Y(yv):.2f}" for xv, yv in zip(x, y))
    safe_title = html.escape(title, quote=True)
    safe_y = html.escape(ylabel, quote=True)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="white"/>
  <text x="{width/2}" y="35" font-size="20" text-anchor="middle">{safe_title}</text>
  <line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#333"/>
  <line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#333"/>
  <polyline points="{points}" stroke="{PALETTE[(channel-1)%len(PALETTE)]}" fill="none" stroke-width="2"/>
  <text x="{width/2}" y="{height-22}" text-anchor="middle" font-size="15">Time (s)</text>
  <text x="23" y="{height/2}" font-size="15" text-anchor="middle" transform="rotate(-90 23 {height/2})">{safe_y}</text>
  <text x="{left}" y="{height-bottom+25}" font-size="12">{x[0]:.4g}</text>
  <text x="{width-right}" y="{height-bottom+25}" font-size="12" text-anchor="end">{x[-1]:.4g}</text>
  <text x="{left-10}" y="{top+5}" text-anchor="end" font-size="12">{ymax:.4g}</text>
  <text x="{left-10}" y="{height-bottom}" text-anchor="end" font-size="12">{ymin:.4g}</text>
</svg>
"""
    return svg


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path, help="Numeric -time recorder output")
    p.add_argument("--output", required=True, type=Path, help="Output SVG image path")
    p.add_argument("--column", type=int, default=1, help="1-based response column, excluding time")
    p.add_argument("--title", default="OpenSees-style recorder output")
    p.add_argument("--ylabel", default="Response (model units)")
    opts = p.parse_args()
    records = read_recorder(opts.input)
    image = svg_chart(records, title=opts.title, ylabel=opts.ylabel, channel=opts.column)
    opts.output.parent.mkdir(parents=True, exist_ok=True)
    opts.output.write_text(image, encoding="utf-8")
    print(f"RESULT=PASS_SIMPLIFIED_RECORDER_PLOT; rows={len(records)}; response_col={opts.column}; file={opts.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
