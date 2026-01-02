import numpy as np


class PerformanceMetrics:
    """
    Economic and service-level performance metrics.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self.total_cost = 0.0
        self.total_demand = 0.0
        self.total_fulfilled = 0.0
        self.stockout_events = 0

    def update(self, demand: float, inventory_after: float, cost: float):
        """
        Update metrics for one time step.

        Parameters
        ----------
        demand : float
            Demand at time t

        inventory_after : float
            Inventory level after demand fulfillment

        cost : float
            Cost incurred at time t
        """
        self.total_cost += cost
        self.total_demand += demand

        fulfilled = demand
        if inventory_after < 0:
            fulfilled = demand + inventory_after
            self.stockout_events += 1

        self.total_fulfilled += max(0.0, fulfilled)

    def results(self) -> dict:
        """
        Return aggregated performance metrics.
        """
        service_level = (
            self.total_fulfilled / self.total_demand
            if self.total_demand > 0
            else 1.0
        )

        return {
            "total_cost": self.total_cost,
            "service_level": service_level,
            "stockout_events": self.stockout_events,
        }
