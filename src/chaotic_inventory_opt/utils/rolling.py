from collections import deque
from typing import Iterable, List


def rolling_window(
    series: Iterable[float],
    window: int,
) -> List[list[float]]:
    """
    Generate rolling windows over a series.

    Parameters
    ----------
    series : iterable of float
        Input time series

    window : int
        Window size (must be > 0)

    Returns
    -------
    list of lists
        Rolling windows
    """
    if window <= 0:
        raise ValueError("window must be positive")

    buffer = deque(maxlen=window)
    windows = []

    for x in series:
        buffer.append(float(x))
        if len(buffer) == window:
            windows.append(list(buffer))

    return windows
