# src/main.py
#!/usr/bin/env python3
"""
Main flow: simulate a Poisson process over many (λ, N) parameter combinations
and histogram their event-time counts, comparing empirical vs theoretical.
Includes clean unit-interval bins and varied RNG.
Only λ, N, tmax (optional), delta, workers, and save_plots vary per run.
"""
import argparse
import sys
import os
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
from typing import List, Tuple, Optional, Any

import numpy as np
import matplotlib.pyplot as plt
from math import exp, factorial, ceil

from poisson_sim import PoissonSim
from histogram import Histogram


def parse_args() -> argparse.Namespace:
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
        help="Width of each histogram bin (unit interval by default)"
    )
    parser.add_argument(
        "--workers", type=int, default=None,
        help="Number of parallel worker processes (None = CPU count)"
    )
    parser.add_argument(
        "--save-plots", action='store_true',
        help="Save histogram and distribution comparison plots as PNG images for each (λ, N)"
    )
    parser.add_argument(
        "--output-dir", type=str, default="histograms",
        help="Directory to save histogram images when --save-plots is set"
    )
    return parser.parse_args()


def poisson_pmf(k: int, mu: float) -> float:
    """Compute the Poisson probability mass function."""
    return (mu ** k) * exp(-mu) / factorial(k)


def run_one(params: Tuple[float, int, Optional[float], float]) -> Tuple[Tuple[float, int], float, List[int], List[float]]:
    """
    Worker: simulate (rate,N), histogram counts per unit interval,
    compare to theoretical Poisson distribution.
    Returns ((rate,N), tmax, counts, edges).
    """
    rate, N, tmax_arg, delta = params
    sim: PoissonSim = PoissonSim(rate=rate, N=N)
    sim.simulate()
    event_times: np.ndarray = sim.get_event_times()

    # determine time horizon
    if tmax_arg is not None:
        tmax: float = tmax_arg
    else:
        tmax = float(np.max(event_times))
    tmax = ceil(tmax / delta) * delta

    # edges from 0 to tmax in steps of delta
    num_intervals: int = int(tmax / delta)
    edges: List[float] = [i * delta for i in range(num_intervals + 1)]

    # empirical counts per interval
    hist: Histogram = Histogram(bins=edges)
    counts, edges = hist.compute(event_times)

    return (rate, N), tmax, counts, edges


def main() -> None:
    args: Any = parse_args()
    if args.save_plots:
        os.makedirs(args.output_dir, exist_ok=True)

    # build tasks
    tasks: List[Tuple[float, int, Optional[float], float]] = [
        (r, n, args.tmax, args.delta)
        for r in args.rates
        for n in args.num_events
    ]

    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        results = list(executor.map(run_one, tasks))

    # textual output if no plots
    if not args.save_plots:
        for (rate, N), tmax, counts, edges in results:
            print(f"λ={rate}, N={N}, tmax={tmax}")
            print(counts)

        # save overlay plots
    if args.save_plots:
        for (rate, N), tmax, counts, edges in results:
            values, freqs = np.unique(counts, return_counts=True)
            num_intervals = len(counts)
            mu: float = rate * args.delta
            theo_freqs: List[float] = [num_intervals * poisson_pmf(k, mu) for k in values]

            plt.figure()
            plt.bar(
                values,
                freqs,
                width=0.8,
                alpha=0.6,
                label='Empirical',
                color='royalblue'  # pastel/navy-ish color
            )
            plt.plot(
                values,
                theo_freqs,
                marker='o',
                linestyle='-',
                label='Theoretical',
                color='salmon'
            )
            plt.xlabel('Events per interval')
            plt.ylabel('Number of intervals')
            plt.title(f'λ={rate}, N={N}')
            plt.legend()

            ts: str = datetime.now().strftime('%Y%m%d_%H%M%S')
            fn: str = f"hist_vs_poisson_l{rate}_N{N}_{ts}.png"
            path: str = os.path.join(args.output_dir, fn)
            plt.tight_layout()
            plt.savefig(path)
            plt.close()
            print(f"Saved plot: {path}")

if __name__ == "__main__":
    main() == "__main__"
