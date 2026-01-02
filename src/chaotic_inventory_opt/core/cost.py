class CostModel:
    """
    Inventory cost model.
    """

    def __init__(
        self,
        holding_cost_per_unit: float,
        stockout_cost_per_unit: float,
        fixed_order_cost: float = 0.0,
    ):
        """
        Parameters
        ----------
        holding_cost_per_unit : float
            Cost per unit of positive inventory per time step

        stockout_cost_per_unit : float
            Cost per unit of unmet demand / backorder per time step

        fixed_order_cost : float
            Fixed cost incurred when an order is placed (optional)
        """
        self.h = float(holding_cost_per_unit)
        self.p = float(stockout_cost_per_unit)
        self.k = float(fixed_order_cost)

    def compute(self, inventory: float, order: float) -> float:
        """
        Compute one-period inventory cost.
        """
        cost = 0.0

        # Stockout / backorder penalty
        if inventory < 0:
            cost += abs(inventory) * self.p
            inventory = 0.0

        # Holding cost
        cost += inventory * self.h

        # Fixed ordering cost
        if order > 0:
            cost += self.k

        return cost
