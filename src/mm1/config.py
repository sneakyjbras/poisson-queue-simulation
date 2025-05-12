# config.py
import argparse
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Config:
    """
    CLI configuration for M/M/1 experiments.

    Attributes:
        lambda_values: list of arrival rates to test
        mu_values: list of service rates to test
        num_events: number of departure events to simulate
        seed: random seed for reproducibility
    """
    lambda_values: List[float]
    mu_values: List[float]
    num_events: int
    seed: Optional[int]

    @staticmethod
    def from_cli() -> "Config":
        parser = argparse.ArgumentParser(
            description="Sweep λ and μ to observe resulting average queue sizes."
        )
        parser.add_argument(
            "--lambda-values", "-l",
            type=float, nargs="+", required=True,
            help="Arrival rates λ to test."
        )
        parser.add_argument(
            "--mu-values", "-m",
            type=float, nargs="+", required=True,
            help="Service rates μ to test."
        )
        parser.add_argument(
            "--num-events", "-n",
            type=int, required=True,
            help="Number of departure events to simulate."
        )
        parser.add_argument(
            "--seed",
            type=int, default=None,
            help="Random seed (optional)."
        )
        args = parser.parse_args()
        return Config(
            lambda_values=args.lambda_values,
            mu_values=args.mu_values,
            num_events=args.num_events,
            seed=args.seed,
        )

