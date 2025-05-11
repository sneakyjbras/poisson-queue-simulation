# plotter.py
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from math import exp, factorial

from config import Config
from result import Result

class Plotter:
    """
    Handles plotting of simulation results: empirical vs theoretical Poisson distribution.
    """
    def __init__(self, config: Config) -> None:
        self.config = config
        if self.config.save_plots:
            os.makedirs(self.config.output_dir, exist_ok=True)

    @staticmethod
    def poisson_pmf(k: int, mu: float) -> float:
        return (mu ** k) * exp(-mu) / factorial(k)

    def plot_count_dist(self, result: Result) -> None:
        values, freqs = np.unique(result.counts, return_counts=True)
        num_intervals = len(result.counts)
        mu = result.rate * self.config.delta
        theo_freqs = [num_intervals * self.poisson_pmf(k, mu) for k in values]

        plt.figure()
        plt.bar(values, freqs, width=0.8, alpha=0.6, color='royalblue', label='Empirical')
        plt.plot(values, theo_freqs, marker='o', linestyle='-', color='salmon', label='Theoretical')
        plt.xlabel('Events per interval')
        plt.ylabel('Number of intervals')
        plt.title(f'λ={result.rate}, N={result.N}')
        plt.legend()

        if self.config.save_plots:
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            fn = f"hist_vs_poisson_l{result.rate}_N{result.N}_{ts}.png"
            path = os.path.join(self.config.output_dir, fn)
            plt.tight_layout()
            plt.savefig(path)
            plt.close()
            print(f"Saved plot: {path}")

