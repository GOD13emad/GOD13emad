#!/usr/bin/env python3
"""Check portfolio claims count, evidence categories and relative file links.
No network, secrets, client files or external datasets are accessed.
"""
from pathlib import Path
from urllib.parse import unquote
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CENTRAL = ROOT / "PORTFOLIO.md"
MATRIX = ROOT / "portfolio/EVIDENCE_MATRIX.md"
ROOT_README = ROOT / "README.md"
DOCS = (
    CENTRAL, MATRIX, ROOT_README,
    ROOT / "ENGINEERING_SERVICES.md",
    ROOT / "FREELANCE_PROFILE_FA.md",
    ROOT / "portfolio/advanced-demos/README.md",
    ROOT / "portfolio/peer-reviewed-and-open-research/README.md",
)
ROW = re.compile(r"^\|\s*(\d{1,2})\s*\|", re.M)
MD_LINK = re.compile(r"!?\[[^\]]*]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
ERRORS = []

def fail(message):
    ERRORS.append(message)
    print("FAIL:", message)

for p in DOCS:
    if not p.is_file():
        fail(f"Missing document: {p.relative_to(ROOT)}")
if ERRORS:
    sys.exit(1)

central = CENTRAL.read_text(encoding="utf-8")
matrix = MATRIX.read_text(encoding="utf-8")
asserted = set(range(1, 27))
for name, content in (("PORTFOLIO.md", central), ("EVIDENCE_MATRIX.md", matrix)):
    ids = [int(n) for n in ROW.findall(content)]
    if len(ids) != 26 or set(ids) != asserted or len(set(ids)) != len(ids):
        fail(f"{name}: expected exactly once numbered entries 01..26, got {ids}")

for name, content in (("PORTFOLIO.md", central), ("EVIDENCE_MATRIX.md", matrix)):
    if "10.17632/csncnv8wnd.2" not in content or "10.17632/xw4shs8hyy.3" not in content:
        fail(f"{name}: missing exact independently verified dataset DOIs")
if "institutional" not in (ROOT / "portfolio/extended-research-prototypes/README.md").read_text(encoding="utf-8").lower():
    fail("Extended research missing third-party institutional ownership caveat")

# Check all published in-repo markdown links across the selected public pages.
for doc in DOCS:
    text = doc.read_text(encoding="utf-8")
    for target in MD_LINK.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "data:", "#", "app://")):
            continue
        file_part = unquote(target.partition("#")[0].partition("?")[0])
        if not file_part:
            continue
        candidate = (doc.parent / file_part).resolve()
        if not candidate.is_relative_to(ROOT.resolve()):
            fail(f"{doc.relative_to(ROOT)}: escaping link {target}")
        elif not candidate.exists():
            fail(f"{doc.relative_to(ROOT)}: missing link {target}")

if ERRORS:
    print(f"PORTFOLIO_EVIDENCE_FAIL errors={len(ERRORS)}")
    sys.exit(1)
print(f"PORTFOLIO_EVIDENCE_PASS docs={len(DOCS)} cases=26 datasets=2 third_party_guard=present")
