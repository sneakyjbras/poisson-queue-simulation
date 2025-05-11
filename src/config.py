# config.py
import argparse
from typing import List, Optional
from dataclasses import dataclass

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

    @staticmethod
    def from_cli() -> 'Config':
        parser = argparse.ArgumentParser(
            description="Simulate Poisson processes for multiple (rate, num-events) combos in parallel."
        )
        parser.add_argument('--rates', type=float, nargs='+', required=True,
                            help='One or more rate (lambda) values')
        parser.add_argument('--num-events', type=int, nargs='+', required=True,
                            help='One or more numbers of events to simulate per rate')
        parser.add_argument('--tmax', type=float, default=None,
                            help='Optional fixed time horizon (dynamic if not set)')
        parser.add_argument('--delta', type=float, default=1.0,
                            help='Width of each histogram bin')
        parser.add_argument('--workers', type=int, default=None,
                            help='Number of parallel worker processes')
        parser.add_argument('--save-plots', action='store_true',
                            help='Save histogram and overlay plots')
        parser.add_argument('--output-dir', type=str, default='histograms',
                            help='Output directory for saved plots')
        args = parser.parse_args()
        return Config(
            rates=args.rates,
            num_events=args.num_events,
            tmax=args.tmax,
            delta=args.delta,
            workers=args.workers,
            save_plots=args.save_plots,
            output_dir=args.output_dir
        )
