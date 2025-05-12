# manager.py
from concurrent.futures import ProcessPoolExecutor
from typing import List

from config import Config
from mm1_sim import MM1Sim
from result import Result


class SimulationManager:
    """
    Coordinates running M/M/1 simulations in parallel based on the given Config.
    """
    def __init__(self, config: Config) -> None:
        self.config: Config = config

    def run_one(self, lam: float, mu: float) -> Result:
        """
        Run a single M/M/1 simulation for given λ and μ and return a Result.
        """
        sim = MM1Sim(
            lam=lam,
            mu=mu,
            max_events=self.config.num_events,
            seed=self.config.seed,
        )
        avg_N, E_T_sys, E_T_q, util = sim.simulate()
        return Result(lam=lam, mu=mu, avg_N=avg_N, E_T_system=E_T_sys, E_T_queue=E_T_q, utilization=util)

    def run_all(self) -> List[Result]:
        """
        Run simulations for all λ and μ combinations in parallel and collect results.
        """
        tasks = [
            (lam, mu)
            for lam in self.config.lambda_values
            for mu in self.config.mu_values
        ]
        results: List[Result] = []
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(self.run_one, lam, mu) for lam, mu in tasks]
            for future in futures:
                results.append(future.result())
        return results

