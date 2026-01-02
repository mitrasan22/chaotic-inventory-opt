import math
from chaotic_inventory_opt.fractal.hurst import HurstEstimator
from chaotic_inventory_opt.chaos.lyapunov import LyapunovExponentEstimator
from chaotic_inventory_opt.regimes.classifier import RegimeClassifier, Regime


class FCIOPolicy:
    def __init__(
        self,
        base_stock_level: float,
        reorder_point: float,
        alpha: float,
        beta: float,
        scale_min: float,
        scale_max: float,
        rho: float,
        gamma: float,
        k_cap: float,
        window: int = 50,
        hurst_estimator=None,
        lyapunov_estimator=None,
        regime_classifier=None,
    ):
        self.S0 = float(base_stock_level)
        self.s = float(reorder_point)

        self.alpha = alpha
        self.beta = beta
        self.scale_min = scale_min
        self.scale_max = scale_max

        self.rho = rho
        self.gamma = gamma
        self.k_cap = k_cap

        self.window = window

        self.hurst = hurst_estimator or HurstEstimator()
        self.lyapunov = lyapunov_estimator or LyapunovExponentEstimator()
        self.regime_classifier = regime_classifier or RegimeClassifier()

        self._demand_buffer = []
        self._H_hist = []
        self._lam_hist = []
        self._backlog = 0.0

    def observe(self, demand: float):
        self._demand_buffer.append(float(demand))
        if len(self._demand_buffer) > self.window:
            self._demand_buffer.pop(0)

        unmet = max(0.0, demand - self._backlog)
        self._backlog = self.rho * self._backlog + unmet

    def order(self, inventory: float) -> float:
        if len(self._demand_buffer) < 10:
            return max(0.0, self.S0 - inventory)

        H_raw = self.hurst.estimate(self._demand_buffer)
        lam_raw = self.lyapunov.estimate(self._demand_buffer)

        self._H_hist.append(H_raw)
        self._lam_hist.append(lam_raw)

        H = sum(self._H_hist[-5:]) / min(len(self._H_hist), 5)
        lam = sum(self._lam_hist[-5:]) / min(len(self._lam_hist), 5)

        raw_scale = math.exp(-self.alpha * lam + self.beta * (H - 0.5))
        scale = min(max(raw_scale, self.scale_min), self.scale_max)

        S_t = self.S0 * scale

        effective_inventory = inventory - self.gamma * self._backlog

        avg_demand = sum(self._demand_buffer) / len(self._demand_buffer)
        k = min(self.k_cap, avg_demand / max(self.S0, 1.0))

        return max(0.0, k * (S_t - effective_inventory))
