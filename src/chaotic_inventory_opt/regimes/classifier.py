from enum import Enum


class Regime(Enum):
    """
    Enumeration of inventory-demand dynamical regimes.
    """

    STABLE = "stable"
    PERSISTENT = "persistent"
    CHAOTIC = "chaotic"
    STRUCTURED_CHAOS = "structured_chaos"


class RegimeClassifier:
    """
    Classifies system regime based on fractal memory and chaos.

    Input:
        H  -> Hurst exponent (memory)
        λ  -> Lyapunov exponent (instability)

    Output:
        Regime enum
    """

    def __init__(
        self,
        hurst_threshold: float = 0.6,
        lyapunov_threshold: float = 0.0,
    ):
        """
        Parameters
        ----------
        hurst_threshold : float
            Threshold above which demand is considered persistent

        lyapunov_threshold : float
            Threshold above which system is considered chaotic
        """
        self.hurst_threshold = hurst_threshold
        self.lyapunov_threshold = lyapunov_threshold

    def classify(self, hurst: float, lyapunov: float) -> Regime:
        """
        Classify the current regime.

        Parameters
        ----------
        hurst : float
            Hurst exponent

        lyapunov : float
            Largest Lyapunov exponent

        Returns
        -------
        Regime
            Classified regime
        """
        if lyapunov > self.lyapunov_threshold and hurst > self.hurst_threshold:
            return Regime.STRUCTURED_CHAOS

        if lyapunov > self.lyapunov_threshold:
            return Regime.CHAOTIC

        if hurst > self.hurst_threshold:
            return Regime.PERSISTENT

        return Regime.STABLE
