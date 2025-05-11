from bisect import bisect_right
from typing import Sequence, List, Tuple, Union, Optional


class Histogram:
    """
    A class to compute histograms (counts and bin edges) for a sequence of numeric data.

    Bins can be specified as an integer number of equal-width bins or as explicit bin edges.
    """

    bins: Union[int, Sequence[float]]
    range: Optional[Tuple[float, float]]

    def __init__(
        self,
        bins: Union[int, Sequence[float]] = 10,
        range: Optional[Tuple[float, float]] = None
    ) -> None:
        """
        Initialize the Histogram.

        :param bins: Number of bins (int) or a sequence of bin edges.
        :param range: Tuple (min, max) specifying the data range if bins is int.
        """
        self.bins = bins
        self.range = range

    def compute(
        self,
        data: Sequence[float]
    ) -> Tuple[List[int], List[float]]:
        """
        Compute the histogram for the given data.

        :param data: Sequence of numeric values.
        :return: A tuple (counts, edges) where:
            - counts: list of integers, number of data points per bin
            - edges: list of floats, length = len(counts) + 1, the bin boundaries
        """
        edges: List[float]
        nbins: int

        if isinstance(self.bins, int):
            if self.range is not None:
                low, high = self.range
            else:
                low, high = float(min(data)), float(max(data))
            width: float = (high - low) / self.bins
            edges = [low + i * width for i in range(self.bins + 1)]
            nbins = self.bins
        else:
            edges = list(self.bins)
            nbins = len(edges) - 1

        counts: List[int] = [0] * nbins

        for x in data:
            if x < edges[0] or x > edges[-1]:
                continue
            if x == edges[-1]:
                idx: int = nbins - 1
            else:
                pos: int = bisect_right(edges, x)
                idx: int = pos - 1
            counts[idx] += 1

        return counts, edges
