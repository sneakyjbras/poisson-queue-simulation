# result.py
from dataclasses import dataclass
from typing import List


@dataclass
class Result:
    """
    Data structure holding the outcome of a single Poisson simulation.

    Attributes:
        rate: Rate (lambda) of the Poisson process.
        N: Number of events simulated.
        tmax: Time horizon used for histogramming.
        counts: Counts per interval (length = num_intervals).
        edges: Bin edges of the histogram.
    """

    rate: float
    N: int
    tmax: float
    counts: List[int]
    edges: List[float]
