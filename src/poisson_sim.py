import numpy as np
from numpy.typing import NDArray

class PoissonSim:
    def __init__(self, lambda_poisson: float, N: int):
        """
        Parameters
        ----------
        lambda_poisson : float
            Rate parameter (events per unit time) for the Poisson process.
        N : int
            Number of events to simulate.
        """
        self.lambda_poisson: float = lambda_poisson
        self.N: int = N

        # Will be filled by simulate()
        self.u:    NDArray[np.float64]
        self.dts:  NDArray[np.float64]
        self.event_times: NDArray[np.float64]

    def simulate(self) -> None:
        """
        Run the simulation: generate uniforms, transform to exponential
        inter-arrival times, and compute event timestamps.
        """
        # 1) draw N uniforms
        self.u = np.random.rand(self.N)
        # 2) inverse‐CDF → exponential gaps
        self.dts = -np.log(1 - self.u) / self.lambda_poisson
        # 3) cumulative sum → arrival times
        self.event_times = np.cumsum(self.dts)

    def get_event_times(self) -> NDArray[np.float64]:
        """Return the array of simulated event timestamps."""
        return self.event_times

    def get_inter_arrivals(self) -> NDArray[np.float64]:
        """Return the array of simulated inter-arrival times."""
        return self.dts

