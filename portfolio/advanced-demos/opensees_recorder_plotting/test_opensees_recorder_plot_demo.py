"""Tests for synthetic OpenSees-style output plotting, not client model."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
import sys

path = Path(__file__).with_name("opensees_recorder_plot_demo.py")
spec = importlib.util.spec_from_file_location("opensees_recorder_plot_demo", path)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class OpenSeesRecorderPlotDemoTests(unittest.TestCase):
    def test_parse_whitespace_comments_and_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp)/"example.out"
            f.write_text("# data from fabricated recorder\n0 0.1 3\n0.5 0.2 4\n1.0 0.3 5\n", encoding="utf8")
            v = module.read_recorder(f)
            self.assertEqual(v, [(0.0, 0.1, 3.0), (0.5, 0.2, 4.0), (1.0, 0.3, 5.0)])

    def test_valid_svg_is_safe_xml(self):
        data = [(0.0, 0.1), (0.5, 0.2), (1.0, 0.3)]
        img = module.svg_chart(data, title="<try>alert & title</try>", ylabel='Displacement "m"')
        doc = ET.fromstring(img)
        self.assertTrue(doc.tag.endswith("svg"))
        self.assertIn("&lt;try&gt;", img)
        self.assertIn("&amp;", img)
        self.assertIn("polyline", img)

    def test_broken_column_count_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp)/"bad.out"
            f.write_text("0 1\n1 2 3\n", encoding="utf8")
            with self.assertRaisesRegex(ValueError, "inconsistent"):module.read_recorder(f)

    def test_non_monotonic_and_non_finite_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp)/"bad.out"
            f.write_text("0 1\n0 2\n", encoding="utf8")
            with self.assertRaisesRegex(ValueError, "strictly increase"):module.read_recorder(f)
            f.write_text("0 1\n1 nan\n", encoding="utf8")
            with self.assertRaisesRegex(ValueError, "nonfinite"):module.read_recorder(f)

    def test_missing_response_column_rejected(self):
        with self.assertRaises(ValueError):
            module.svg_chart([(0.0, 1.0), (1.0, 2.0)], channel=2)

    def test_constant_response_renders(self):
        x = [(0.0, 5.0), (1.0, 5.0)]
        self.assertIn("<polyline", module.svg_chart(x))

    def test_read_comma_separator(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp)/"out.csv"
            f.write_text("0, 0.2\n1, -0.1\n", encoding="utf8")
            self.assertEqual(module.read_recorder(f), [(0.0, 0.2), (1.0, -0.1)])

    def test_few_samples_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp)/"one.out"
            f.write_text("0 1\n", encoding="utf8")
            with self.assertRaisesRegex(ValueError, "at least two"):module.read_recorder(f)


if __name__ == "__main__":
    unittest.main()
