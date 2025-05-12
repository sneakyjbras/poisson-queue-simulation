# result.py
from dataclasses import dataclass

@dataclass
class Result:
    """
    Holds the outcome of one M/M/1 simulation scenario.
    """
    lam: float
    mu: float
    target_queue_size: float
    E_T_system: float
    E_T_queue: float
    utilization: float
