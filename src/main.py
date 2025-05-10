# main.py
#!/usr/bin/env python3
"""
Main flow: simulate a Poisson process over many (λ, N) parameter combinations
and histogram their event times in parallel using Python-level concurrency.
All parameters except λ and N are fixed.
"""
import argparse
import sys
from concurrent.futures import ProcessPoolExecutor
from typing import List, Tuple

from poisson_sim import PoissonSim
from histogram import Histogram

# Fixed parameters
T_MAX = 10.0    # Maximum time horizon for histogram
DELTA = 1.0     # Width of each histogram bin
WORKERS = None  # Number of parallel worker processes (None = CPU count)


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
    return parser.parse_args()


def run_one(params: Tuple[float, int]) -> Tuple[Tuple[float, int], List[int], List[float]]:
    """
    Worker function: simulate and histogram for a single (rate, N).
    Uses fixed T_MAX and DELTA.
    Returns a tuple ((rate, N), counts, edges).
    """
    rate, N = params
    sim = PoissonSim(rate=rate, N=N)
    sim.simulate()
    event_times = sim.get_event_times()

    n_bins = int(T_MAX / DELTA)
    hist = Histogram(bins=n_bins, range=(0.0, T_MAX))
    counts, edges = hist.compute(event_times)

    return (rate, N), counts, edges


def main():
    args = parse_args()

    # Build parameter grid with fixed T_MAX and DELTA
    tasks = [
        (rate, N)
        for rate in args.rates
        for N    in args.num_events
    ]

    # Parallel execution
    try:
        with ProcessPoolExecutor(max_workers=WORKERS) as executor:
            results = list(executor.map(run_one, tasks))
    except Exception as e:
        print(f"Error during parallel execution: {e}", file=sys.stderr)
        sys.exit(1)

    # Output aggregated results
    print("Parallel Poisson Simulation Histogram Results:")
    print(f"Time horizon: [0, {T_MAX}], Bin width: {DELTA}\n")
    print(f"{'Rate':>6} {'N':>8} {'Bin Start':>10} {'Bin End':>10} {'Count':>8}")
    print("" + "-" * 50)
    for (rate, N), counts, edges in results:
        for start, end, count in zip(edges[:-1], edges[1:], counts):
            print(f"{rate:6.2f} {N:8d} {start:10.2f} {end:10.2f} {count:8d}")

if __name__ == "__main__":
    main()

