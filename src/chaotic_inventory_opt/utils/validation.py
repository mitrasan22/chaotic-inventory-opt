import numpy as np


def validate_series(series, min_length: int = 1):
    """
    Validate a numeric time series.

    Parameters
    ----------
    series : array-like
        Time series data

    min_length : int
        Minimum required length

    Returns
    -------
    np.ndarray
        Validated numeric array
    """
    x = np.asarray(series, dtype=float)

    if len(x) < min_length:
        raise ValueError(
            f"Series length {len(x)} < required minimum {min_length}"
        )

    if np.any(np.isnan(x)):
        raise ValueError("Series contains NaN values")

    if np.any(np.isinf(x)):
        raise ValueError("Series contains infinite values")

    return x


def validate_positive(value: float, name: str = "value"):
    """
    Validate that a scalar is non-negative.

    Parameters
    ----------
    value : float
        Value to validate

    name : str
        Variable name (for error messages)
    """
    if value < 0:
        raise ValueError(f"{name} must be non-negative")
