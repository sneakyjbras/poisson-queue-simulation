# config.py
import argparse
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Config:
    """
    CLI configuration for the Poisson simulation.

    Attributes:
        rates: List of lambda values.
        num_events: List of event counts N.
        tmax: Optional fixed time horizon.
        delta: Bin width.
        workers: Number of parallel workers.
        save_plots: Flag to save plots.
        output_dir: Directory for saved images.
    """

    rates: List[float]
    num_events: List[int]
    tmax: Optional[float]
    delta: float
    workers: Optional[int]
    save_plots: bool
    output_dir: str
    superimpose: bool
    seed: int

    @staticmethod
    def from_cli() -> "Config":
        parser = argparse.ArgumentParser(
            description="Simulate Poisson processes for multiple (rate, num-events) combos in parallel."
        )
        parser.add_argument(
            "--rates",
            type=float,
            nargs="+",
            required=True,
            help="One or more rate (lambda) values",
        )
        parser.add_argument(
            "--num-events",
            type=int,
            nargs="+",
            required=True,
            help="One or more numbers of events to simulate per rate",
        )
        parser.add_argument(
            "--tmax",
            type=float,
            default=None,
            help="Optional fixed time horizon (dynamic if not set)",
        )
        parser.add_argument(
            "--delta", type=float, default=1.0, help="Width of each histogram bin"
        )
        parser.add_argument(
            "--workers",
            type=int,
            default=None,
            help="Number of parallel worker processes",
        )
        parser.add_argument(
            "--save-plots", action="store_true", help="Save histogram and overlay plots"
        )
        parser.add_argument(
            "--output-dir",
            type=str,
            default="histograms",
            help="Output directory for saved plots",
        )
        parser.add_argument(
            "--superimpose",
            action="store_true",
            help="Enable superposition: combine multiple processes into one simulation",
        )
        parser.add_argument(
            "--seed",
            type=int,
            default=None,
            help="Random seed (optional).",
        )
        args = parser.parse_args()
        return Config(
            rates=args.rates,
            num_events=args.num_events,
            tmax=args.tmax,
            delta=args.delta,
            workers=args.workers,
            save_plots=args.save_plots,
            output_dir=args.output_dir,
            superimpose=args.superimpose,
            seed=args.seed,
        )
