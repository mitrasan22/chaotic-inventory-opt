import numpy as np


class SampleEntropy:
    """
    Sample entropy estimator for time series complexity.
    """

    def __init__(
        self,
        m: int = 2,
        r_ratio: float = 0.2,
    ):
        """
        Parameters
        ----------
        m : int
            Embedding dimension

        r_ratio : float
            Tolerance as a fraction of series standard deviation
        """
        self.m = m
        self.r_ratio = r_ratio

    def estimate(self, series) -> float:
        """
        Estimate sample entropy.

        Parameters
        ----------
        series : array-like

        Returns
        -------
        float
            Sample entropy value
        """
        x = np.asarray(series, dtype=float)
        N = len(x)

        if N <= self.m + 1:
            return 0.0

        r = self.r_ratio * np.std(x)

        def _count(m):
            patterns = np.array([x[i:i + m] for i in range(N - m)])
            count = 0
            for i in range(len(patterns)):
                dist = np.max(np.abs(patterns - patterns[i]), axis=1)
                count += np.sum(dist < r) - 1
            return count

        Cm = _count(self.m)
        Cm1 = _count(self.m + 1)

        if Cm == 0 or Cm1 == 0:
            return 0.0

        return float(-np.log(Cm1 / Cm))
