# main.py
import random
from typing import List
from config import Config
from mm1_sim import MM1Sim
from result import Result

def main() -> None:
    """
    Parse CLI arguments, run M/M/1 simulations for each scenario, collect results,
    and then print them in a structured way.
    """
    config = Config.from_cli()
    if config.seed is not None:
        random.seed(config.seed)

    results: List[Result] = []

    for lam in config.lambda_values:
        for target in config.target_queue_sizes:
            if target <= 0:
                continue
            rho = target / (1 + target)
            if lam == 0:
                # trivial empty system
                results.append(Result(lam, float('nan'), target, 0.0, 0.0, 0.0))
                continue
            mu = lam / rho
            sim = MM1Sim(lam=lam, mu=mu, sim_time=config.sim_time, seed=None)
            E_T_system, E_T_queue, utilization = sim.simulate()
            results.append(
                Result(
                    lam=lam,
                    mu=mu,
                    target_queue_size=target,
                    E_T_system=E_T_system,
                    E_T_queue=E_T_queue,
                    utilization=utilization,
                )
            )

    # Print a table of results
    print(f"{'λ':>6} {'μ':>8} {'E[N]ₜₐr₉':>8} {'E[T_sys]':>10} {'E[T_q]':>10} {'Util%':>8}")
    print("-" * 56)
    for r in results:
        print(f"{r.lam:6.2f} {r.mu:8.2f} {r.target_queue_size:8.0f} "
              f"{r.E_T_system:10.4f} {r.E_T_queue:10.4f} {r.utilization*100:8.2f}")

if __name__ == "__main__":
    main()

