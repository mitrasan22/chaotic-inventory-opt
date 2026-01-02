from chaotic_inventory_opt.control.fcio import FCIOPolicy


class NetworkFCIOPolicy:
    """
    FCIO policy for multi-SKU inventory networks.
    """

    def __init__(self, policies: dict[str, FCIOPolicy]):
        """
        Parameters
        ----------
        policies : dict
            Mapping SKU -> FCIOPolicy
        """
        self.policies = policies

    def observe(self, demand_dict: dict[str, float]):
        """
        Observe demands for all SKUs.
        """
        for sku, demand in demand_dict.items():
            policy = self.policies[sku]
            if hasattr(policy, "observe"):
                policy.observe(demand)


    def order(self, inventory_dict: dict[str, float]) -> dict[str, float]:
        """
        Compute orders for all SKUs.
        """
        orders = {}

        for sku, inventory in inventory_dict.items():
            orders[sku] = self.policies[sku].order(inventory)

        return orders
