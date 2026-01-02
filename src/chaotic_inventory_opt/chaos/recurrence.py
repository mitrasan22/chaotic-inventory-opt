import numpy as np


class RecurrenceAnalyzer:
    """
    Recurrence Quantification Analysis (RQA).

    Computes recurrence-based chaos metrics.
    """

    def __init__(
        self,
        threshold_ratio: float = 0.1,
    ):
        """
        Parameters
        ----------
        threshold_ratio : float
            Distance threshold as fraction of series std
        """
        self.threshold_ratio = threshold_ratio

    def recurrence_matrix(self, series):
        """
        Compute recurrence matrix.

        Parameters
        ----------
        series : array-like

        Returns
        -------
        np.ndarray
            Binary recurrence matrix
        """
        x = np.asarray(series, dtype=float)
        N = len(x)

        if N < 10:
            return np.zeros((N, N))

        eps = self.threshold_ratio * np.std(x)
        dist = np.abs(x[:, None] - x[None, :])

        return (dist < eps).astype(int)

    def recurrence_rate(self, series) -> float:
        """
        Recurrence rate (RR).

        Fraction of recurrent points.
        """
        R = self.recurrence_matrix(series)
        if R.size == 0:
            return 0.0
        return float(np.sum(R) / R.size)
