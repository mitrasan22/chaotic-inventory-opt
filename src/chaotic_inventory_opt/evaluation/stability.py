import numpy as np
from chaotic_inventory_opt.chaos.lyapunov import LyapunovExponentEstimator


class StabilityMetrics:
    """
    Stability and chaos metrics for inventory trajectories.
    """

    def __init__(
        self,
        lyapunov_estimator: LyapunovExponentEstimator,
        window: int = 50,
    ):
        self.lyapunov = lyapunov_estimator
        self.window = window
        self.reset()

    def reset(self):
        self._inventory_trace = []

    def update(self, inventory: float):
        """
        Update stability metrics with new inventory level.
        """
        self._inventory_trace.append(inventory)

        if len(self._inventory_trace) > self.window:
            self._inventory_trace.pop(0)

    def results(self) -> dict:
        """
        Return stability metrics.
        """
        variance = float(np.var(self._inventory_trace)) if self._inventory_trace else 0.0
        lyap = (
            self.lyapunov.estimate(self._inventory_trace)
            if len(self._inventory_trace) >= 10
            else 0.0
        )

        return {
            "inventory_variance": variance,
            "lyapunov_exponent": lyap,
        }
