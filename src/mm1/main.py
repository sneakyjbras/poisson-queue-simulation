# main.py
from typing import List

from config import Config
from manager import SimulationManager
from result import Result


def main() -> None:
    # Parse CLI and set RNG seed
    cfg: Config = Config.from_cli()
    if cfg.seed is not None:
        import numpy as np

        np.random.seed(cfg.seed)

    # Delegate all simulation work to SimulationManager
    manager: SimulationManager = SimulationManager(cfg)
    results: List[Result] = manager.run_all()

    # Print formatted table of results with both simulated and theoretical values
    header: str = (
        f"{'λ':>8} {'μ':>8} "
        f"{'E[N]_sim':>10} {'E[T_sys]_sim':>12} {'E[T_q]_sim':>12} {'Util%_sim':>10} "
        f"{'E[N]_theo':>10} {'E[T_sys]_theo':>12} {'E[T_q]_theo':>12} {'Util%_theo':>10}"
    )
    print(header)
    print("=" * len(header))

    for r in results:
        print(
            f"{r.lam:8.2f} {r.mu:8.2f} "
            f"{r.avg_N:10.2f} {r.E_T_system:12.2f} {r.E_T_queue:12.2f} {r.utilization*100:10.2f} "
            f"{r.theo_avg_N:10.2f} {r.theo_E_T_system:12.2f} {r.theo_E_T_queue:12.2f} {r.theo_utilization*100:10.2f}"
        )
        print()


if __name__ == "__main__":
    main()
