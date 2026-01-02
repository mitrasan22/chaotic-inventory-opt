class EOQPolicy:
    """
    Economic Order Quantity (EOQ) policy.

    Assumes deterministic average demand.
    """

    def __init__(self, order_quantity: float):
        self.Q = float(order_quantity)

    def order(self, inventory: float) -> float:
        """
        EOQ places a fixed order when inventory is depleted.
        """
        if inventory <= 0:
            return self.Q
        return 0.0


class BaseStockPolicy:
    """
    Base-stock (order-up-to) policy.
    """

    def __init__(self, base_stock_level: float):
        self.S = float(base_stock_level)

    def order(self, inventory: float) -> float:
        """
        Order up to the base-stock level.
        """
        return max(0.0, self.S - inventory)


class sSPolicy:
    """
    (s,S) reorder point policy.
    """

    def __init__(self, reorder_point: float, order_up_to: float):
        if order_up_to <= reorder_point:
            raise ValueError("S must be greater than s")

        self.s = float(reorder_point)
        self.S = float(order_up_to)

    def order(self, inventory: float) -> float:
        """
        Place order if inventory drops below s.
        """
        if inventory < self.s:
            return self.S - inventory
        return 0.0
