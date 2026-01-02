import yaml
import pandas as pd
import numpy as np
from pathlib import Path

from chaotic_inventory_opt.control.classical import sSPolicy, BaseStockPolicy
from chaotic_inventory_opt.control.fcio import FCIOPolicy
from chaotic_inventory_opt.core.inventory_system import InventorySystem
from chaotic_inventory_opt.core.cost import CostModel
from chaotic_inventory_opt.evaluation.performance import PerformanceMetrics
from chaotic_inventory_opt.evaluation.stability import StabilityMetrics
from chaotic_inventory_opt.chaos.lyapunov import LyapunovExponentEstimator


CONFIG_PATH = Path(__file__).parents[1] / "configs" / "fcio.yaml"

with open(CONFIG_PATH) as f:
    cfg = yaml.safe_load(f)


# ----------------------------
# Load multiple SKUs
# ----------------------------
sales = pd.read_csv(cfg["data"]["path"])
d_cols = [c for c in sales.columns if c.startswith("d_")]

subset = sales.sample(cfg["data"]["num_skus"], random_state=42)
demand_matrix = subset[d_cols].values.astype(float)


# ----------------------------
# Policy factory
# ----------------------------
def make_policy():
    p = cfg["policy"]

    if p["type"] == "sS":
        return sSPolicy(p["reorder_point"], p["order_up_to"])

    if p["type"] == "base_stock":
        return BaseStockPolicy(p["base_stock_level"])

    if p["type"] == "fcio":
        return FCIOPolicy(
            base_stock_level=p["base_stock_level"],
            reorder_point=p["reorder_point"],
            alpha=p["alpha"],
            beta=p["beta"],
            window=p["window"],
            scale_min=p["scale_min"],
            scale_max=p["scale_max"],
            rho=p["rho"],
            gamma=p["gamma"],
            k_cap=p["k_cap"],
        )

    raise ValueError("Unknown policy type")


# ----------------------------
# Init systems
# ----------------------------
N, T = demand_matrix.shape

systems = [InventorySystem(cfg["system"]["initial_inventory"]) for _ in range(N)]
policies = [make_policy() for _ in range(N)]

cost_model = CostModel(**cfg["cost"])
perf = PerformanceMetrics()
stab = StabilityMetrics(LyapunovExponentEstimator())


# ----------------------------
# Simulation
# ----------------------------
for t in range(T):
    demands = demand_matrix[:, t]

    for i in range(N):
        if hasattr(policies[i], "observe"):
            policies[i].observe(demands[i])

    for i in range(N):
        q = policies[i].order(systems[i].I)
        inv = systems[i].step(demands[i], q)
        cost = cost_model.compute(inv, q)

        perf.update(demands[i], inv, cost)
        stab.update(inv)


print("Performance:", perf.results())
print("Stability:", stab.results())
