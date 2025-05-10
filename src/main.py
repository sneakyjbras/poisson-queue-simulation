# main.py
#!/usr/bin/env python3
"""
Main flow: simulate a Poisson process over many (λ, N) parameter combinations
and histogram their event times in parallel, with optional fixed or dynamic time horizon,
and variable bin width (delta) and worker count.
Only λ, N, tmax (optional), delta, and workers vary per run.
"""
import argparse
import sys
from concurrent.futures import ProcessPoolExecutor
from typing import List, Tuple, Optional
import numpy as np

from poisson_sim import PoissonSim
from histogram import Histogram


def parse_args():
    parser = argparse.ArgumentParser(
        description="Simulate Poisson processes for multiple (rate, num-events) combos in parallel."
    )
    parser.add_argument(
        "--rates", type=float, nargs='+', required=True,
        help="One or more rate (λ) values for the Poisson process"
    )
    parser.add_argument(
        "--num-events", type=int, nargs='+', required=True,
        help="One or more numbers of events to simulate per rate"
    )
    parser.add_argument(
        "--tmax", type=float, default=None,
        help="Optional fixed maximum time horizon for histogram (dynamic if not set)"
    )
    parser.add_argument(
        "--delta", type=float, default=1.0,
        help="Width of each histogram bin"
    )
    parser.add_argument(
        "--workers", type=int, default=None,
        help="Number of parallel worker processes (None = CPU count)"
    )
    return parser.parse_args()


def run_one(params: Tuple[float, int, Optional[float], float]) -> Tuple[Tuple[float, int], float, List[int], List[float]]:
    """
    Worker function: simulate for a single (rate, N).
    If tmax_arg is provided, uses fixed time horizon; otherwise computes dynamic tmax = max(event_times).
    Bins of width delta.
    Returns ((rate, N), tmax, counts, edges).
    """
    rate, N, tmax_arg, delta = params
    sim = PoissonSim(rate=rate, N=N)
    sim.simulate()
    event_times = sim.get_event_times()

    # Choose time horizon
    if tmax_arg is not None:
        tmax = tmax_arg
    else:
        tmax = float(np.max(event_times))

    # Compute bins
    n_bins = int(np.ceil(tmax / delta))
    edges = [i * delta for i in range(n_bins + 1)]

    hist = Histogram(bins=edges)
    counts, edges = hist.compute(event_times)

    return (rate, N), tmax, counts, edges


def main():
    args = parse_args()

    # Build parameter grid, include tmax override and delta
    tasks = [
        (rate, N, args.tmax, args.delta)
        for rate in args.rates
        for N    in args.num_events
    ]

    # Parallel execution with specified workers
    try:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            results = list(executor.map(run_one, tasks))
    except Exception as e:
        print(f"Error during parallel execution: {e}", file=sys.stderr)
        sys.exit(1)

    # Output aggregated results
    print("Parallel Poisson Simulation Histogram Results:")
    print(f"Bin width: {args.delta}\n")
    header = f"{'Rate':>6} {'N':>8} {'T_max':>8} {'Bin Start':>10} {'Bin End':>10} {'Count':>8}"
    print(header)
    print("" + "-" * len(header))
    for (rate, N), tmax, counts, edges in results:
        for start, end, count in zip(edges[:-1], edges[1:], counts):
            print(f"{rate:6.2f} {N:8d} {tmax:8.2f} {start:10.2f} {end:10.2f} {count:8d}")

if __name__ == "__main__":
    main()

