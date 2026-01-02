import copy
import numpy as np


class RobustnessEvaluator:
    """
    Robustness evaluation via demand shocks and perturbations.
    """

    def __init__(self, shock_probability: float, shock_magnitude: float):
        """
        Parameters
        ----------
        shock_probability : float
            Probability of demand shock at each time step

        shock_magnitude : float
            Multiplicative shock factor (e.g., 2.0 means doubling demand)
        """
        self.shock_probability = shock_probability
        self.shock_magnitude = shock_magnitude

    def apply_shocks(self, demand_series):
        """
        Apply random demand shocks.

        Returns
        -------
        np.ndarray
            Shocked demand series
        """
        demand = np.asarray(demand_series, dtype=float)
        shocked = demand.copy()

        for t in range(len(shocked)):
            if np.random.rand() < self.shock_probability:
                shocked[t] *= self.shock_magnitude

        return shocked
