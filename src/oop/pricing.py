"""Skew-Gosset option pricing formulas from Section 2.3."""

from collections.abc import Callable

import numpy as np
from scipy import integrate


def truncated_density(
    z: float,
    density_fn: Callable[[float], float],
    x_p: float,
    x_c: float,
) -> float:
    """Implements Eq. (S2.Ex4)."""
    if z < x_p or z > x_c:
        return 0.0
    return float(density_fn(z))


def compute_z_normalizer(
    sigma_t: float,
    density_fn: Callable[[float], float],
    x_p: float,
    x_c: float,
    p_p: float,
    p_c: float,
) -> float:
    """Implements Eq. (S2.Ex5) first term."""

    def integrand(z: float) -> float:
        return np.exp(sigma_t * z) * truncated_density(z, density_fn, x_p, x_c) / (p_c - p_p)

    val, _ = integrate.quad(integrand, x_p, x_c, limit=200)
    return float(val)


def skew_gosset_call_price(
    s0: float,
    r: float,
    t: float,
    k_t: float,
    sigma_t: float,
    density_fn: Callable[[float], float],
    x_p: float,
    x_c: float,
    p_p: float,
    p_c: float,
) -> float:
    """Implements Eq. (S2.Ex6) with Eq. (S2.Ex5)."""
    z = compute_z_normalizer(sigma_t, density_fn, x_p, x_c, p_p, p_c)
    a_t = s0 * np.exp(r * t) / z
    lower = np.log(k_t / a_t) / sigma_t

    def integrand(val: float) -> float:
        return (a_t * np.exp(sigma_t * val) - k_t) * truncated_density(val, density_fn, x_p, x_c) / (p_c - p_p)

    price, _ = integrate.quad(integrand, lower, x_c, limit=200)
    return float(price)


def skew_gosset_put_price(
    s0: float,
    r: float,
    t: float,
    k_t: float,
    sigma_t: float,
    density_fn: Callable[[float], float],
    x_p: float,
    x_c: float,
    p_p: float,
    p_c: float,
) -> float:
    """Implements Eq. (S2.Ex7) with Eq. (S2.Ex5)."""
    z = compute_z_normalizer(sigma_t, density_fn, x_p, x_c, p_p, p_c)
    a_t = s0 * np.exp(r * t) / z
    upper = np.log(k_t / a_t) / sigma_t

    def integrand(val: float) -> float:
        return (k_t - a_t * np.exp(sigma_t * val)) * truncated_density(val, density_fn, x_p, x_c) / (p_c - p_p)

    price, _ = integrate.quad(integrand, x_p, upper, limit=200)
    return float(price)
