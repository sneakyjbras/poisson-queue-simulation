from typing import Optional
import numpy as np


class PoissonSim:
    """
    Simulates a Poisson process by generating inter-arrival times
    and cumulative event times using a given rate (lambda).
    """

    def __init__(self, rate: float, N: int) -> None:
        """
        Initialize the simulator.

        :param rate: The rate (lambda) of the Poisson process.
        :param N: The number of events to simulate.
        """
        self.rate: float = rate
        self.N: int = N
        # Attributes set after simulation
        self.u: Optional[np.ndarray] = None
        self.dts: Optional[np.ndarray] = None

    def simulate(self) -> None:
        """
        Perform the simulation of inter-arrival times and event times.
        """
        # Generate uniform random numbers
        self.u = np.random.rand(self.N)
        # Transform to exponential inter-arrival times
        self.dts = -np.log(1 - self.u) / self.rate

    def get_inter_arrivals(self) -> np.ndarray:
        """
        Get the simulated inter-arrival times.

        :return: Array of inter-arrival times of length N.
        :raises RuntimeError: If simulate() has not been called yet.
        """
        if self.dts is None:
            raise RuntimeError("simulate() must be called before accessing inter-arrival times.")
        return self.dts
