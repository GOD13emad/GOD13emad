# Synthetic Online Congestion-Game Route Choice

**Status:** Original independent numerical demonstration; **five local Windows unit tests passed on 29 October 2026 and were rerun successfully on 31 October 2026** (Python 3.14.7, `unittest` 5 tests, `exitCode=0`; synthetic test inputs only). No actual dispatch customer, vehicle telemetry, paper replication, commercial MATLAB licence, client agreement, or deployed routing platform is involved.

This self-contained Python 3.11+ standard-library example models **six synthetic drivers** arriving sequentially at **two parallel alternatives** with occupancy-dependent travel-time proxy costs. Each arrival is assigned to the current least-cost route; existing drivers can then make strictly beneficial unilateral route switches. It is a small **atomic congestion game**, not a vehicle-routing problem with pickup/dropoff, time windows, road-network topology or uncertain traffic.

| Synthetic model check | Locally observed |
|---|---:|
| Final occupancy | 2 drivers on A, 4 on B |
| Total travel-time proxy | 47.48 driver-minutes |
| Static all-on-shortest-route comparison | 165 driver-minutes |
| Maximum unilateral improvement possible at final state | 0.0 minutes |
| Standalone unit tests | 5 / 5 PASS |

These numbers are *only for the constructed parameters*. They do not imply measured transport savings or superiority over a customer's existing algorithm. The counterfactual intentionally uses a congestion-unaware static assignment and is **not** a globally optimized or mathematically fair comparison to all offline planning methods.

## Reproduce

```bash
python synthetic_online_congestion_game_demo.py
python -m unittest discover -s . -p "test_synthetic_online_congestion_game_demo.py" -v
```

No third-party packages, datasets, credentials or network calls are needed.

**Source:** [synthetic_online_congestion_game_demo.py](synthetic_online_congestion_game_demo.py)  
**Tests:** [test_synthetic_online_congestion_game_demo.py](test_synthetic_online_congestion_game_demo.py)

The project's public methodology is evidence-first: use synthetic examples only as skills demonstrations, and require authentic project inputs, acceptance criteria and legally licensed tools before offering paid work.
