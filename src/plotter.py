# plotter.py
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from math import exp, factorial
from typing import List

from config import Config
from result import Result

class Plotter:
    """
    Handles plotting of simulation results: empirical vs theoretical Poisson distribution.
    """

    config: Config

    def __init__(self, config: Config) -> None:
        self.config = config
        if self.config.save_plots:
            os.makedirs(self.config.output_dir, exist_ok=True)

    @staticmethod
    def poisson_pmf(k: int, mu: float) -> float:
        """
        Compute the Poisson probability mass function at k given mean mu.
        """
        return (mu ** k) * exp(-mu) / factorial(k)

    def plot_count_dist(self, result: Result) -> None:
        """
        Plot the empirical histogram of counts vs. theoretical Poisson distribution.
        """
        values: np.ndarray
        freqs: np.ndarray
        values, freqs = np.unique(result.counts, return_counts=True)

        num_intervals: int = len(result.counts)
        mu: float = result.rate * self.config.delta
        theo_freqs: List[float] = [num_intervals * self.poisson_pmf(int(k), mu) for k in values]

        plt.figure()
        plt.bar(values, freqs, width=0.8, alpha=0.6, color='royalblue', label='Empirical')
        plt.plot(values, theo_freqs, marker='o', linestyle='-', color='salmon', label='Theoretical')
        plt.xlabel('Events per interval')
        plt.ylabel('Number of intervals')
        plt.title(f'λ={result.rate}, N={result.N}')
        plt.legend()

        if self.config.save_plots:
            ts: str = datetime.now().strftime('%Y%m%d_%H%M%S')
            fn: str = f"hist_vs_poisson_l{result.rate}_N{result.N}_{ts}.png"
            path: str = os.path.join(self.config.output_dir, fn)
            plt.tight_layout()
            plt.savefig(path)
            plt.close()
            print(f"Saved plot: {path}")
