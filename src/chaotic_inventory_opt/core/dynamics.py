import numpy as np


class InventoryDynamics:
    """
    Dynamical system analysis for inventory control.
    """

    @staticmethod
    def jacobian(dQ_dI: float) -> float:
        """
        Jacobian of inventory map:
            J = 1 + dQ/dI
        """
        return 1.0 + dQ_dI

    @staticmethod
    def lyapunov_from_jacobians(jacobians) -> float:
        """
        Estimate Lyapunov exponent from Jacobian sequence.
        """
        J = np.asarray(jacobians, dtype=float)

        if len(J) == 0:
            return 0.0

        return float(np.mean(np.log(np.abs(J) + 1e-12)))
