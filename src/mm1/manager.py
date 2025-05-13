# manager.py
from concurrent.futures import Future, ProcessPoolExecutor
from typing import List, Tuple

from config import Config
from mm1_sim import MM1Sim
from result import Result


class SimulationManager:
    """
    Coordinates running M/M/1 simulations in parallel based on the given Config,
    and computes theoretical metrics for each run.
    """

    def __init__(self, config: Config) -> None:
        self.config: Config = config

    def run_one(self, lam: float, mu: float) -> Result:
        """
        Run a single M/M/1 simulation for given λ and μ and return a Result,
        including both simulated and theoretical metrics.
        """
        sim = MM1Sim(
            lam=lam,
            mu=mu,
            max_events=self.config.num_events,
            seed=self.config.seed,
        )
        avg_N, E_T_sys, E_T_q, util = sim.simulate()

        # Compute theoretical values (stable only if lam < mu)
        rho = lam / mu
        if lam < mu:
            theo_L = rho / (1 - rho)
            theo_W = 1.0 / (mu - lam)
            theo_Wq = theo_W - 1.0 / mu
        else:
            theo_L = float("inf")
            theo_W = float("inf")
            theo_Wq = float("inf")
        theo_util = rho

        return Result(
            lam=lam,
            mu=mu,
            avg_N=avg_N,
            E_T_system=E_T_sys,
            E_T_queue=E_T_q,
            utilization=util,
            theo_avg_N=theo_L,
            theo_E_T_system=theo_W,
            theo_E_T_queue=theo_Wq,
            theo_utilization=theo_util,
        )

    def run_all(self) -> List[Result]:
        """
        Run simulations for all λ and μ combinations in parallel and collect results.
        """
        tasks: List[Tuple[float, float]] = [
            (lam, mu)
            for lam in self.config.lambda_values
            for mu in self.config.mu_values
        ]
        results: List[Result] = []

        with ProcessPoolExecutor() as executor:
            futures: List[Future[Result]] = [
                executor.submit(self.run_one, lam, mu) for lam, mu in tasks
            ]
            for future in futures:
                results.append(future.result())

        return results
