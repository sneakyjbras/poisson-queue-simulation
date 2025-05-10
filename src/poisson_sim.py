import numpy as np
from numpy.typing import NDArray

class PoissonSim:
    def __init__(self, lambda_poisson: float, N: int):
        """
        Simulate a homogeneous Poisson process of rate λ over N events.

        Parameters
        ----------
        lambda_poisson : float
            Rate (events per unit time) of the Poisson process.
        N : int
            Number of inter-arrival times and events to generate.
        """
        self.lambda_poisson: float = lambda_poisson
        self.N: int = N

        # placeholders for simulated data
        self.u:           NDArray[np.float64]
        self.dts:         NDArray[np.float64]
        self.event_times: NDArray[np.float64]

    def simulate(self) -> None:
        """
        Generate the process: uniforms, inter-arrival times, and event timestamps.
        """
        # 1) Draw N Uniform(0,1) samples
        self.u = np.random.rand(self.N)
        # 2) Transform to Exp(lambda_poisson) gaps via inverse-CDF
        self.dts = -np.log(1 - self.u) / self.lambda_poisson
        # 3) Cumulative sum to get absolute event times
        self.event_times = np.cumsum(self.dts)

    def get_inter_arrivals(self) -> NDArray[np.float64]:
        """Return the simulated inter-arrival times (Δt_i)."""
        return self.dts

    def get_event_times(self) -> NDArray[np.float64]:
        """Return the absolute arrival times S_n."""
        return self.event_times

    def inter_arrival_pdf(self) -> NDArray[np.float64]:
        """
        Evaluate the exponential PDF at each inter-arrival: f_T(Δt_i) = λ e^{-λ Δt_i}.

        Returns
        -------
        NDArray[np.float64]
            Array of PDF values corresponding to each Δt.
        """
        return self.lambda_poisson * np.exp(-self.lambda_poisson * self.dts)

    def counts_per_interval(self, delta: float = 1.0) -> NDArray[np.int_]:
        """
        Count number of events in non-overlapping intervals of width delta.

        Parameters
        ----------
        delta : float
            Width of each time interval (default is 1.0).

        Returns
        -------
        NDArray[np.int_]
            Array of event counts per interval.
        """
        # Define bin edges from 0 to last event time, step delta
        T_max = self.event_times[-1]
        bins = np.arange(0, T_max + delta, delta)
        counts, _ = np.histogram(self.event_times, bins=bins)
        return counts

    def plot_counts_histogram(self, delta: float = 1.0) -> None:
        """
        Plot histogram of event counts per interval of width delta.

        Parameters
        ----------
        delta : float
            Width of each time interval for grouping events.
        """
        import matplotlib.pyplot as plt

        counts = self.counts_per_interval(delta)
        # Create bin edges to center bars on integer counts
        bins = np.arange(0, counts.max() + 2) - 0.5
        plt.hist(counts, bins=bins, align='mid', edgecolor='black')
        plt.xlabel(f'Number of events per {delta}-unit interval')
        plt.ylabel('Frequency')
        plt.title(f'Histogram of counts per {delta}-unit interval')
        plt.show()

