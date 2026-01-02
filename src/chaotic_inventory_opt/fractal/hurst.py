import numpy as np


class HurstEstimator:
    """
    Estimate the Hurst exponent of a time series.

    The Hurst exponent quantifies long-range dependence:
        H > 0.5  -> persistent
        H = 0.5  -> memoryless
        H < 0.5  -> mean-reverting
    """

    def __init__(
        self,
        min_lag: int = 2,
        max_lag: int = 20,
    ):
        """
        Parameters
        ----------
        min_lag : int
            Minimum lag used in scaling analysis

        max_lag : int
            Maximum lag used in scaling analysis
        """
        if min_lag < 1:
            raise ValueError("min_lag must be >= 1")
        if max_lag <= min_lag:
            raise ValueError("max_lag must be > min_lag")

        self.min_lag = min_lag
        self.max_lag = max_lag

    def estimate(self, series) -> float:
        import numpy as np

        x = np.asarray(series, dtype=float)

        if len(x) < self.max_lag + 1:
            return 0.5

        lags = []
        tau = []

        for lag in range(self.min_lag, self.max_lag + 1):
            diff = x[lag:] - x[:-lag]
            std = np.std(diff)

            if std > 1e-8: 
                lags.append(lag)
                tau.append(std)

        if len(tau) < 2:
            return 0.5

        lags = np.array(lags)
        tau = np.array(tau)

        slope, _ = np.polyfit(np.log(lags), np.log(tau), 1)
        return float(slope)

