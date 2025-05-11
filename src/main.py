# main.py
#!/usr/bin/env python3
"""
Main flow: simulate a Poisson process over many (λ, N) parameter combinations
and histogram their event-time counts, comparing empirical vs theoretical.
Uses a mock simulation function in PoissonSim for now.
Only λ, N, tmax (optional), delta, workers, and save_plots vary per run.
"""
import argparse
import sys
import os
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
from typing import List, Tuple, Optional

import numpy as np
import matplotlib.pyplot as plt
from math import exp, factorial

from poisson_sim import PoissonSim  # expects a mock_simulate method
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
    Worker function: simulate for a single (rate, N) using a mock simulate.
    If tmax_arg is provided, uses fixed time horizon; otherwise computes dynamic tmax = max(event_times).
    Bins of width delta.
    Returns ((rate, N), tmax, counts, edges).
    """
    rate, N, tmax_arg, delta = params
    sim = PoissonSim(rate=rate, N=N)
    # Use a mock simulation method for now
    sim.simulate()
    # Get the event times from 
    event_times = sim.get_event_times()

    # Choose time horizon
    tmax = tmax_arg if tmax_arg is not None else float(np.max(event_times))

    # Compute bins
    n_bins = int(np.ceil(tmax / delta))
    edges = [i * delta for i in range(n_bins + 1)]

    hist = Histogram(bins=edges)
    counts, edges = hist.compute(event_times)

    return (rate, N), tmax, counts, edges


def main():
    args = parse_args()

    # Prepare output directory if saving plots
    if args.save_plots:
        os.makedirs(args.output_dir, exist_ok=True)

    # Build parameter grid
    tasks = [
        (rate, N, args.tmax, args.delta)
        for rate in args.rates
        for N in args.num_events
    ]

    # Run in parallel
    try:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            results = list(executor.map(run_one, tasks))
    except Exception as e:
        print(f"Error during parallel execution: {e}", file=sys.stderr)
        sys.exit(1)

    # Print or save
    if not args.save_plots:
        print("Results (empirical vs theoretical counts per bin):")
        for (rate, N), tmax, counts, edges in results:
            print(f"λ={rate}, N={N}, t_max={tmax:.2f}")
            print(counts)

    if args.save_plots:
        for (rate, N), tmax, counts, edges in results:
            # 1) Build empirical histogram of counts-per-bin
            values, freqs = np.unique(counts, return_counts=True)
            n_bins = len(counts)

            # 2) Compute theoretical frequencies:
            #    expected #bins with k events = n_bins * P(Pois(λΔ)=k)
            mu = rate * args.delta
            theo_freqs = [n_bins * poisson_pmf(k, mu) for k in values]

            # 3) Plot empirical vs. theoretical
            plt.figure()
            plt.bar(values, freqs, width=0.6, alpha=0.7, label='Empirical')
            plt.plot(values, theo_freqs, marker='o', linestyle='-', label='Theoretical')
            plt.xlabel('Events per interval')
            plt.ylabel('Number of bins')
            plt.title(f'λ={rate}, N={N}, Δ={args.delta}')
            plt.legend()

            # 4) Save with timestamped filename
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            fname = f"hist_vs_poisson_l{rate}_N{N}_{ts}.png"
            path = os.path.join(args.output_dir, fname)
            plt.tight_layout()
            plt.savefig(path)
            plt.close()
            print(f"Saved plot: {path}")
 
if __name__ == "__main__":
    main()

