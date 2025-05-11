from typing import Optional

import numpy as np


class PoissonSim:
    """
    Simulates a Poisson process by generating inter-arrival times
    and cumulative event times using a given rate (lambda).
    """

    rate: float
    N: int
    u: Optional[np.ndarray]
    dts: Optional[np.ndarray]
    event_times: Optional[np.ndarray]

    def __init__(self, rate: float, N: int) -> None:
        """
        Initialize the simulator.

        :param rate: The rate (lambda) of the Poisson process.
        :param N: The number of events to simulate.
        """
        self.rate = rate
        self.N = N
        self.u = None
        self.dts = None
        self.event_times = None

    def simulate(self) -> None:
        """
        Perform the simulation of inter-arrival times and event times.
        """
        self.u = np.random.rand(self.N)
        self.dts = -np.log(1 - self.u) / self.rate
        self.event_times = np.cumsum(self.dts)

    def get_inter_arrivals(self) -> np.ndarray:
        """
        Get the simulated inter-arrival times.

        :return: Array of inter-arrival times of length N.
        :raises RuntimeError: If simulate() has not been called yet.
        """
        if self.dts is None:
            raise RuntimeError(
                "simulate() must be called before accessing inter-arrival times."
            )
        return self.dts

    def get_event_times(self) -> np.ndarray:
        """
        Get the cumulative event times.

        :return: Array of event times of length N.
        :raises RuntimeError: If simulate() has not been called yet.
        """
        if self.event_times is None:
            raise RuntimeError(
                "simulate() must be called before accessing event times."
            )
        return self.event_times
