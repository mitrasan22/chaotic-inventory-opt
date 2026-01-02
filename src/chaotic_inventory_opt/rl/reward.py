from chaotic_inventory_opt.chaos.lyapunov import LyapunovExponentEstimator


class RewardFunction:
    """
    Reward function combining economic cost and chaos penalty.
    """

    def __init__(
        self,
        chaos_weight: float,
        lyapunov_estimator: LyapunovExponentEstimator,
        window: int = 50,
    ):
        self.chaos_weight = chaos_weight
        self.lyapunov = lyapunov_estimator
        self.window = window
        self._inventory_trace = []

    def compute(self, inventory: float, cost: float) -> float:
        """
        Compute reward.
        """
        self._inventory_trace.append(inventory)

        if len(self._inventory_trace) > self.window:
            self._inventory_trace.pop(0)

        chaos_penalty = 0.0
        if len(self._inventory_trace) >= 10:
            chaos_penalty = self.lyapunov.estimate(self._inventory_trace)

        return -cost - self.chaos_weight * chaos_penalty
