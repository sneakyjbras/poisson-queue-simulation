# manager.py
import os
from concurrent.futures import Future, ProcessPoolExecutor
from math import ceil
from typing import List, Tuple

import numpy as np

from config import Config
from histogram import Histogram
from poisson_sim import PoissonSim
from result import Result


class SimulationManager:
    """
    Coordinates running Poisson simulations in parallel based on a Config.
    """

    config: Config

    def __init__(self, config: Config) -> None:
        self.config = config
        if self.config.save_plots:
            os.makedirs(self.config.output_dir, exist_ok=True)

    @staticmethod
    def simulate_process(rate: float, N: int) -> List[float]:
        """Simulate a Poisson process and return its event times."""
        sim = PoissonSim(rate=rate, N=N)
        sim.simulate()
        return sim.get_event_times().tolist()

    def run_one(self, rate: float, N: int) -> Result:
        """
        Run a single Poisson simulation and return a Result object.
        """
        sim: PoissonSim = PoissonSim(rate=rate, N=N)
        sim.simulate()
        event_times: List[float] = sim.get_event_times()

        # Determine tmax and bin edges
        tmax: float = (
            self.config.tmax
            if self.config.tmax is not None
            else float(np.max(event_times))
        )
        tmax = ceil(tmax / self.config.delta) * self.config.delta
        num_intervals: int = int(tmax / self.config.delta)
        edges: List[float] = [i * self.config.delta for i in range(num_intervals + 1)]

        # Histogram calculation
        hist: Histogram = Histogram(bins=edges)
        counts, edges = hist.compute(event_times)

        return Result(rate, N, tmax, counts, edges)

    def run_all(self) -> List[Result]:
        """
        Run all configured simulation scenarios.
        """
        results: List[Result] = []
        if not self.config.superimpose:
            # Original behavior: simulate each (rate, N) separately
            tasks = [(r, n) for r in self.config.rates for n in self.config.num_events]
            with ProcessPoolExecutor(max_workers=self.config.workers) as executor:
                futures = [executor.submit(self.run_one, rate, N) for rate, N in tasks]
                for future in futures:
                    results.append(future.result())
        else:
            # Superposition mode: combine multiple processes
            with ProcessPoolExecutor(max_workers=self.config.workers) as executor:
                for N in self.config.num_events:
                    # Simulate N events for each rate in parallel
                    futures = [
                        executor.submit(SimulationManager.simulate_process, rate, N)
                        for rate in self.config.rates
                    ]
                    event_time_lists = [future.result() for future in futures]
                    # Determine shortest time horizon across all processes
                    final_times = [
                        times[-1] for times in event_time_lists if len(times) > 0
                    ]
                    if final_times:
                        T_max = float(np.min(final_times))
                    else:
                        T_max = 0.0
                    # Optionally constrain horizon by config.tmax (do not exceed T_max)
                    if self.config.tmax is not None:
                        horizon = float(self.config.tmax)
                        if horizon > T_max:
                            horizon = T_max
                    else:
                        horizon = T_max
                    # Truncate each process's events to the horizon and merge
                    truncated_times: List[float] = []
                    for times in event_time_lists:
                        for t in times:
                            if t <= horizon:
                                truncated_times.append(t)
                            else:
                                break  # stop, as times are sorted
                    truncated_times.sort()
                    # Use horizon as tmax for histogram
                    tmax = horizon
                    # Compute bin edges from 0 to tmax with bin width delta
                    if tmax > 0:
                        num_full_bins = int(tmax // self.config.delta)
                        edges = [
                            i * self.config.delta for i in range(num_full_bins + 1)
                        ]
                        if len(edges) == 0 or edges[0] != 0.0:
                            edges.insert(0, 0.0)
                        if edges[-1] < tmax:
                            edges.append(tmax)
                    else:
                        edges = [0.0]
                    # Compute histogram counts for truncated combined events
                    hist = Histogram(bins=edges)
                    counts, edges = hist.compute(truncated_times)
                    # Prepare Result with summed rate and combined event count (events ≤ horizon)
                    total_rate = float(np.sum(self.config.rates))
                    total_events = len(truncated_times)
                    results.append(
                        Result(total_rate, total_events, tmax, counts, edges)
                    )
        return results
