import numpy as np

try:
    import pywt
except ImportError as e:
    raise ImportError(
        "wavelets module requires 'pywt'. "
        "Install via: pip install PyWavelets"
    ) from e


class WaveletEnergyAnalyzer:
    """
    Multi-scale wavelet energy analysis.

    Decomposes a time series into wavelet coefficients
    and computes energy at each scale.
    """

    def __init__(
        self,
        wavelet: str = "db4",
        max_level: int | None = None,
    ):
        """
        Parameters
        ----------
        wavelet : str
            Wavelet family (e.g., 'db4', 'haar', 'sym5')

        max_level : int or None
            Maximum decomposition level.
            If None, inferred from data length.
        """
        self.wavelet = wavelet
        self.max_level = max_level

    def decompose(self, series):
        """
        Perform discrete wavelet decomposition.

        Parameters
        ----------
        series : array-like
            Time series data

        Returns
        -------
        list[np.ndarray]
            Wavelet coefficient arrays
        """
        x = np.asarray(series, dtype=float)

        if self.max_level is None:
            max_level = pywt.dwt_max_level(
                data_len=len(x),
                filter_len=pywt.Wavelet(self.wavelet).dec_len
            )
        else:
            max_level = self.max_level

        coeffs = pywt.wavedec(x, self.wavelet, level=max_level)
        return coeffs

    def energy_by_scale(self, series) -> dict:
        """
        Compute energy at each wavelet scale.

        Parameters
        ----------
        series : array-like
            Time series data

        Returns
        -------
        dict
            Mapping: scale -> normalized energy
        """
        coeffs = self.decompose(series)

        energies = []
        for c in coeffs[1:]:  # skip approximation
            energies.append(np.sum(c ** 2))

        total_energy = np.sum(energies)

        if total_energy == 0:
            return {}

        return {
            f"scale_{i+1}": float(e / total_energy)
            for i, e in enumerate(energies)
        }

    def energy_slope(self, series) -> float:
        """
        Estimate scaling exponent of wavelet energy.

        For fractal signals, energy across scales follows:
            E(j) ~ j^{-α}

        Returns
        -------
        float
            Estimated scaling slope (α)
        """
        energy = self.energy_by_scale(series)

        if len(energy) < 2:
            return 0.0

        scales = np.arange(1, len(energy) + 1)
        values = np.array(list(energy.values()))

        slope, _ = np.polyfit(np.log(scales), np.log(values), 1)
        return float(-slope)
