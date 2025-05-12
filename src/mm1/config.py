# config.py
import argparse
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Config:
    """
    Configuration for the M/M/1 queue simulation loaded from CLI arguments.
    
    Attributes:
        lambda_values: List of arrival rates (λ) to simulate.
        target_queue_sizes: List of target average queue sizes (E[N]) to simulate.
        sim_time: Total simulation time horizon.
        seed: Optional random seed for reproducibility.
    """
    lambda_values: List[float]
    target_queue_sizes: List[float]
    sim_time: float
    seed: Optional[int]

    @staticmethod
    def from_cli() -> "Config":
        """
        Parse command-line arguments and create a Config instance.
        
        :return: Config object populated with CLI parameters.
        """
        parser = argparse.ArgumentParser(description="Simulate an M/M/1 queue for given parameters.")
        parser.add_argument(
            "--lambda-values",
            type=float,
            nargs="+",
            required=True,
            help="One or more arrival rate (λ) values."
        )
        parser.add_argument(
            "--target-queue-sizes",
            type=float,
            nargs="+",
            required=True,
            help="One or more target average queue sizes (E[N]) for simulation."
        )
        parser.add_argument(
            "--sim-time",
            type=float,
            required=True,
            help="Total simulation time horizon."
        )
        parser.add_argument(
            "--seed",
            type=int,
            default=None,
            help="Optional random seed for reproducibility."
        )
        args = parser.parse_args()
        return Config(
            lambda_values=args.lambda_values,
            target_queue_sizes=args.target_queue_sizes,
            sim_time=args.sim_time,
            seed=args.seed
        )

