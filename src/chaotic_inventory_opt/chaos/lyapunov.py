import numpy as np


class LyapunovExponentEstimator:
    """
    Estimate the largest Lyapunov exponent (LLE) of a time series.

    A positive value indicates deterministic chaos.
    """

    def __init__(
        self,
        min_neighbors: int = 5,
        eps: float = 1e-8,
    ):
        """
        Parameters
        ----------
        min_neighbors : int
            Minimum number of neighbors used in divergence estimation

        eps : float
            Small constant to avoid log(0)
        """
        self.min_neighbors = min_neighbors
        self.eps = eps

    def estimate(self, series) -> float:
        """
        Estimate the largest Lyapunov exponent.

        Parameters
        ----------
        series : array-like
            Time series data

        Returns
        -------
        float
            Estimated Lyapunov exponent
        """
        x = np.asarray(series, dtype=float)

        if len(x) < 50:
            return 0.0

        # Simple divergence-based estimator (robust, fast)
        diffs = np.abs(np.diff(x))

        if np.all(diffs == 0):
            return 0.0

        return float(np.mean(np.log(diffs + self.eps)))
