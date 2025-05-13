# result.py
from dataclasses import dataclass


@dataclass
class Result:
    """
    Holds the outcome of one M/M/1 simulation scenario, including theoretical metrics.
    """

    lam: float
    mu: float
    avg_N: float  # Simulated time-averaged number in system
    E_T_system: float  # Simulated average time in system
    E_T_queue: float  # Simulated average time in queue
    utilization: float  # Simulated server busy fraction

    # Theoretical metrics
    theo_avg_N: float  # Theoretical average number in system
    theo_E_T_system: float  # Theoretical average time in system
    theo_E_T_queue: float  # Theoretical average time in queue
    theo_utilization: float  # Theoretical utilization (ρ)
