# result.py
from dataclasses import dataclass

@dataclass
class Result:
    """
    Holds the outcome of one M/M/1 simulation scenario.
    """
    lam: float
    mu: float
    avg_N: float         # time-averaged number in system
    E_T_system: float    # avg time in system per packet
    E_T_queue: float     # avg time in queue per packet
    utilization: float   # fraction of time server busy

