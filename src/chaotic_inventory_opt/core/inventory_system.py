class InventorySystem:
    """
    Inventory system state and evolution.

    Mathematical model:
        I_{t+1} = I_t + Q_t - D_t
    """

    def __init__(self, initial_inventory: float):
        self.I = float(initial_inventory)

    def step(self, demand: float, order: float) -> float:
        """
        Advance inventory by one time step.

        Parameters
        ----------
        demand : float
            Demand at time t
        order : float
            Order quantity Q_t

        Returns
        -------
        float
            Inventory level at time t+1
        """
        self.I = self.I + order - demand
        return self.I

    def reset(self, inventory: float):
        """
        Reset inventory state.
        """
        self.I = float(inventory)
