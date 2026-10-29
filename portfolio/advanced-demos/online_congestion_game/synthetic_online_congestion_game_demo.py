#!/usr/bin/env python3
"""ORIGINAL SYNTHETIC example: incremental congestion-game route choice.

Pure Python standard library; NOT any marketplace client's algorithm, data,
reference paper, real traffic model or licensed MATLAB implementation.
Illustrates best-response convergence in a small parallel-route congestion game.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
import json
from typing import Iterable


@dataclass(frozen=True)
class Route:
    name: str
    free_flow_min: float
    capacity: float
    alpha: float = 0.4
    beta: float = 2.0

    def __post_init__(self):
        if not self.name or self.free_flow_min <= 0 or self.capacity <= 0:
            raise ValueError("Route name, free-flow time and capacity must be valid")
        if self.alpha < 0 or self.beta < 1:
            raise ValueError("Congestion parameters outside supported range")

    def latency(self, users: int) -> float:
        if not isinstance(users, int) or users < 0:
            raise ValueError("users must be a nonnegative integer")
        return self.free_flow_min * (1.0 + self.alpha * (users / self.capacity) ** self.beta)


def _state(routes: tuple[Route, ...], allocation: dict[str, str]) -> dict:
    counts = Counter(allocation.values())
    by_name = {r.name: r for r in routes}
    per_agent_latency = {agent: by_name[path].latency(counts[path])
                         for agent, path in allocation.items()}
    regrets = []
    for agent, current_path in allocation.items():
        current_cost = per_agent_latency[agent]
        best_alternative = min(
            (r.latency(counts[r.name] + 1) for r in routes if r.name != current_path),
            default=current_cost)
        regrets.append(max(0.0, current_cost - best_alternative))
    return {
        "assignment": dict(sorted(allocation.items())),
        "flows": {r.name: counts[r.name] for r in routes},
        "mean_latency_min": round(sum(per_agent_latency.values()) / len(allocation), 8),
        "total_latency_min": round(sum(per_agent_latency.values()), 8),
        "maximum_unilateral_regret_min": round(max(regrets, default=0.0), 8),
    }


def online_best_response(routes: Iterable[Route], arriving_drivers: Iterable[str]) -> dict:
    """On each arrival, pick current cheapest route, then re-balance via best responses.

    Assumes parallel routes, simultaneous occupancy and BPR-style latency.
    Does NOT model pickup/dropoff, road topology, windows or customer's paper.
    """
    routes = tuple(routes)
    drivers = tuple(arriving_drivers)
    if len(routes) < 2 or len(set(r.name for r in routes)) != len(routes):
        raise ValueError("At least two uniquely named routes are required")
    if not drivers or any(not d for d in drivers) or len(set(drivers)) != len(drivers):
        raise ValueError("Nonempty unique driver labels required")
    allocation: dict[str, str] = {}
    stages = []
    for driver in drivers:
        counts = Counter(allocation.values())
        best = min(routes, key=lambda r: (r.latency(counts[r.name] + 1), r.name))
        allocation[driver] = best.name
        switches = 0
        # Finite congestion games possess a potential: strict best responses terminate.
        for _ in range(100 * len(allocation) ** 2):
            changed = False
            counts = Counter(allocation.values())
            for a in tuple(allocation):
                current = allocation[a]
                current_cost = next(r for r in routes if r.name == current).latency(counts[current])
                alternative = min(routes, key=lambda r: (
                    r.latency(counts[r.name] + (r.name != current)), r.name))
                alt_cost = alternative.latency(counts[alternative.name] +
                                                (alternative.name != current))
                if alternative.name != current and alt_cost < current_cost - 1e-10:
                    allocation[a] = alternative.name
                    counts[current] -= 1
                    counts[alternative.name] += 1
                    switches += 1
                    changed = True
            if not changed:
                break
        else:
            raise RuntimeError("Best responses failed to converge")
        stage = _state(routes, allocation)
        stage["new_driver"] = driver
        stage["best_response_switches"] = switches
        stages.append(stage)
    final = stages[-1]
    # Offline shortest-free-flow choice ignores congestion.
    shortest = min(routes, key=lambda r: (r.free_flow_min, r.name))
    naive_total = len(drivers) * shortest.latency(len(drivers))
    return {
        "label": "INDEPENDENT_SYNTHETIC_TOY_ONLY",
        "assumptions": "two-or-more parallel routes; occupancy-based BPR-style cost; no real traffic",
        "stages": stages,
        "final": final,
        "naive_all_shortest_total_latency_min": round(naive_total, 8),
        "offline_shortest_route_name": shortest.name,
    }


def demo() -> dict:
    routes = (
        Route("A_short_narrow", free_flow_min=5.0, capacity=2.0, alpha=0.5),
        Route("B_long_wide", free_flow_min=7.0, capacity=5.0, alpha=0.25),
    )
    return online_best_response(routes, ["d1", "d2", "d3", "d4", "d5", "d6"])


if __name__ == "__main__":
    print(json.dumps(demo(), ensure_ascii=False, indent=2))
