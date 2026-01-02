"""
chaotic_inventory_opt
=====================

Fractal-Chaotic Inventory Optimization (FCIO)

A dataset-agnostic inventory optimization library that treats
inventory systems as nonlinear dynamical systems and stabilizes
them using fractal analysis and chaos theory.

Core ideas:
- Inventory dynamics as feedback control systems
- Fractal demand (long-range dependence)
- Deterministic chaos and predictability limits
- Chaos-aware and stability-centric inventory control

Public API:
-----------
Users typically interact with the library via:

    from chaotic_inventory_opt.control.fcio import fcio_policy

The library itself is independent of any specific dataset and
operates on generic demand time series.

Author: Santanu Mitra
License: MIT
"""

__version__ = "0.1.0"

from chaotic_inventory_opt.control.fcio import FCIOPolicy
from chaotic_inventory_opt.control.classical import sSPolicy
from chaotic_inventory_opt.regimes.classifier import RegimeClassifier

__all__ = [
    "FCIOPolicy",
    "sSPolicy",
    "RegimeClassifier",
]
