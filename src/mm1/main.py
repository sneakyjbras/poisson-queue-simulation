import random
from typing import List

from config import Config
from manager import SimulationManager
from result import Result


def main() -> None:
    # Parse CLI and set RNG seed
    cfg: Config = Config.from_cli()
    if cfg.seed is not None:
        random.seed(cfg.seed)

    # Delegate all simulation work to SimulationManager
    manager: SimulationManager = SimulationManager(cfg)
    results: List[Result] = manager.run_all()

    # Print formatted table of results with sparser, human-readable large numbers
    header: str = (
        f"{'λ':>8} {'μ':>10} {'E[N]_sim':>15} {'E[T_sys]':>15} {'E[T_q]':>15} {'Util%':>10}"
    )
    print(header)
    print("=" * len(header))

    for r in results:
        # Use thousands separators or scientific notation for large numbers
        print(
            f"{r.lam:8.2f} {r.mu:10.2f} {r.avg_N:15,.2f} "
            f"{r.E_T_system:15,.2f} {r.E_T_queue:15,.2f} {r.utilization*100:10.2f}"
        )
        print()  # blank line for sparser output


if __name__ == "__main__":
    main()
