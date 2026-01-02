import yaml
import pandas as pd
from pathlib import Path

from chaotic_inventory_opt.control.classical import sSPolicy, BaseStockPolicy
from chaotic_inventory_opt.control.fcio import FCIOPolicy
from chaotic_inventory_opt.core.inventory_system import InventorySystem
from chaotic_inventory_opt.core.cost import CostModel
from chaotic_inventory_opt.evaluation.performance import PerformanceMetrics
from chaotic_inventory_opt.evaluation.stability import StabilityMetrics
from chaotic_inventory_opt.chaos.lyapunov import LyapunovExponentEstimator


# ----------------------------
# Load config
# ----------------------------
CONFIG_PATH = Path(__file__).parents[1] / "configs" / "fcio.yaml"

with open(CONFIG_PATH) as f:
    cfg = yaml.safe_load(f)


# ----------------------------
# Load demand (M5)
# ----------------------------
def load_m5(item_id, store_id):
    sales = pd.read_csv(cfg["data"]["path"])
    row = sales[
        (sales["item_id"] == item_id) &
        (sales["store_id"] == store_id)
    ]
    d_cols = [c for c in row.columns if c.startswith("d_")]
    return row[d_cols].values.flatten().astype(float)


demand = load_m5(cfg["data"]["item_id"], cfg["data"]["store_id"])


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


policy = make_policy()


# ----------------------------
# Cost + system
# ----------------------------
cost_model = CostModel(**cfg["cost"])
system = InventorySystem(cfg["system"]["initial_inventory"])

perf = PerformanceMetrics()
stab = StabilityMetrics(LyapunovExponentEstimator())


# ----------------------------
# Simulation
# ----------------------------
for d in demand:
    if hasattr(policy, "observe"):
        policy.observe(d)

    q = policy.order(system.I)
    inv = system.step(d, q)

    cost = cost_model.compute(inv, q)
    perf.update(d, inv, cost)
    stab.update(inv)


print("Performance:", perf.results())
print("Stability:", stab.results())
