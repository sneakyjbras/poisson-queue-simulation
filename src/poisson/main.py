# main.py
#!/usr/bin/env python3
"""
Entry point: parses CLI, runs simulations, and delegates to Plotter.
"""
from typing import List

from config import Config
from manager import SimulationManager
from plotter import Plotter
from result import Result  # Assuming this exists for type hinting


def main() -> None:
    config: Config = Config.from_cli()
    # Seed NumPy RNG if provided
    if config.seed is not None:
        import numpy as np

        np.random.seed(config.seed)

    manager: SimulationManager = SimulationManager(config)
    results: List[SimulationResult] = manager.run_all()

    plotter: Plotter = Plotter(config)
    for res in results:
        plotter.plot_count_dist(res)

    if not config.save_plots:
        for res in results:
            print(res)


if __name__ == "__main__":
    main()
