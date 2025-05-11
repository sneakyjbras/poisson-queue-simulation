# manager.py
import os
from concurrent.futures import ProcessPoolExecutor, Future
from typing import List, Tuple
import numpy as np
from math import ceil

from poisson_sim import PoissonSim
from histogram import Histogram
from config import Config
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

    def run_one(self, rate: float, N: int) -> Result:
        """
        Run a single Poisson simulation and return a Result object.
        """
        sim: PoissonSim = PoissonSim(rate=rate, N=N)
        sim.simulate()
        event_times: List[float] = sim.get_event_times()

        # Determine tmax and bin edges
        tmax: float = self.config.tmax if self.config.tmax is not None else float(np.max(event_times))
        tmax = ceil(tmax / self.config.delta) * self.config.delta
        num_intervals: int = int(tmax / self.config.delta)
        edges: List[float] = [i * self.config.delta for i in range(num_intervals + 1)]

        # Histogram calculation
        hist: Histogram = Histogram(bins=edges)
        counts, edges = hist.compute(event_times)

        return Result(rate, N, tmax, counts, edges)

    def run_all(self) -> List[Result]:
        """
        Run all configured (rate, num_events) pairs in parallel.
        """
        tasks: List[Tuple[float, int]] = [
            (r, n)
            for r in self.config.rates
            for n in self.config.num_events
        ]

        results: List[Result] = []
        with ProcessPoolExecutor(max_workers=self.config.workers) as executor:
            futures: List[Future[Result]] = [
                executor.submit(self.run_one, rate, N) for rate, N in tasks
            ]
            for future in futures:
                results.append(future.result())

        return results
