# main.py
#!/usr/bin/env python3
"""
Entry point: parses CLI, runs simulations, and delegates to Plotter.
"""
from config import Config
from manager import SimulationManager
from plotter import Plotter


def main() -> None:
    config = Config.from_cli()
    manager = SimulationManager(config)
    results = manager.run_all()

    plotter = Plotter(config)
    for res in results:
        plotter.plot_count_dist(res)

    if not config.save_plots:
        for res in results:
            print(res)

if __name__ == '__main__':
    main()

