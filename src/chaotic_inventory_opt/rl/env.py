import numpy as np
from chaotic_inventory_opt.core.inventory_system import InventorySystem
from chaotic_inventory_opt.core.cost import CostModel


class InventoryEnv:
    """
    Gym-style inventory environment.

    State:
        [inventory_level, recent_demand_mean, recent_demand_std]

    Action:
        order quantity (float >= 0)
    """

    def __init__(
        self,
        demand_series,
        initial_inventory: float,
        cost_model: CostModel,
        window: int = 10,
    ):
        self.demand = np.asarray(demand_series, dtype=float)
        self.window = window
        self.t = 0

        self.system = InventorySystem(initial_inventory)
        self.cost_model = cost_model

        self._demand_buffer = []

    def reset(self):
        self.t = 0
        self.system.reset(self.system.I)
        self._demand_buffer.clear()
        return self._get_state()

    def step(self, action: float):
        """
        Execute one environment step.
        """
        demand_t = self.demand[self.t]
        self._demand_buffer.append(demand_t)

        if len(self._demand_buffer) > self.window:
            self._demand_buffer.pop(0)

        inventory_next = self.system.step(demand_t, action)
        cost = self.cost_model.compute(inventory_next, action)

        self.t += 1
        done = self.t >= len(self.demand) - 1

        return self._get_state(), -cost, done, {}

    def _get_state(self):
        """
        Construct state representation.
        """
        if not self._demand_buffer:
            mean_d = 0.0
            std_d = 0.0
        else:
            mean_d = float(np.mean(self._demand_buffer))
            std_d = float(np.std(self._demand_buffer))

        return np.array([self.system.I, mean_d, std_d], dtype=float)
