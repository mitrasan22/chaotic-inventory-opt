import numpy as np


class RSAnalysis:
    """
    Rescaled Range (R/S) analysis for Hurst exponent estimation.
    """

    def __init__(self, window_sizes=None):
        """
        Parameters
        ----------
        window_sizes : list[int] or None
            Window sizes for R/S computation.
            If None, defaults are inferred from data length.
        """
        self.window_sizes = window_sizes

    def estimate(self, series) -> float:
        """
        Estimate Hurst exponent using R/S analysis.

        Parameters
        ----------
        series : array-like
            Time series data

        Returns
        -------
        float
            Estimated Hurst exponent
        """
        x = np.asarray(series, dtype=float)
        N = len(x)

        if N < 50:
            return 0.5

        if self.window_sizes is None:
            self.window_sizes = [10, 20, 50, 100, 200]

        rs_values = []
        sizes = []

        for size in self.window_sizes:
            if size >= N:
                continue

            num_segments = N // size
            rs_segment = []

            for i in range(num_segments):
                segment = x[i * size:(i + 1) * size]
                mean = np.mean(segment)
                cumulative_dev = np.cumsum(segment - mean)
                R = np.max(cumulative_dev) - np.min(cumulative_dev)
                S = np.std(segment)

                if S > 0:
                    rs_segment.append(R / S)

            if rs_segment:
                rs_values.append(np.mean(rs_segment))
                sizes.append(size)

        if len(rs_values) < 2:
            return 0.5

        slope, _ = np.polyfit(np.log(sizes), np.log(rs_values), 1)
        return float(slope)
