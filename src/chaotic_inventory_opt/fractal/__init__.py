"""
Fractal analysis module.

This module provides tools to quantify long-range dependence
and memory structure in demand time series.
"""

from .hurst import HurstEstimator
from .rs_analysis import RSAnalysis

__all__ = [
    "HurstEstimator",
    "RSAnalysis",
]
