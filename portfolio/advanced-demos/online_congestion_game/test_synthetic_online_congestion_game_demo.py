"""Tests for original synthetic example, no client data or external network."""
import importlib.util
from pathlib import Path
import unittest

path=Path(__file__).with_name("synthetic_online_congestion_game_demo.py")
spec=importlib.util.spec_from_file_location("synthetic_demo",path)
mod=importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name]=mod
spec.loader.exec_module(mod)


class RouteTests(unittest.TestCase):
    def test_cost_increases_with_occupancy(self):
        route=mod.Route("a",free_flow_min=7,capacity=2)
        self.assertLess(route.latency(2),route.latency(3))

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            mod.Route("",2,1)
        with self.assertRaises(ValueError):
            mod.online_best_response((mod.Route("a",2,1),),("d1",))
        with self.assertRaises(ValueError):
            mod.online_best_response((mod.Route("a",2,1),mod.Route("b",3,1)),("d1","d1"))

    def test_each_arrival_has_unique_assignment(self):
        v=mod.demo()
        for i,s in enumerate(v["stages"],1):
            self.assertEqual(len(s["assignment"]),i)
            self.assertEqual(sum(s["flows"].values()),i)
            self.assertLessEqual(s["maximum_unilateral_regret_min"],1e-7)

    def test_congestion_rebalancing_outperforms_naive_on_toy(self):
        result=mod.demo()
        self.assertLess(result["final"]["total_latency_min"],
                        result["naive_all_shortest_total_latency_min"])

    def test_deterministic_and_no_real_data(self):
        self.assertEqual(mod.demo(),mod.demo())
        self.assertEqual(mod.demo()["label"],"INDEPENDENT_SYNTHETIC_TOY_ONLY")


if __name__ == "__main__":
    unittest.main()
