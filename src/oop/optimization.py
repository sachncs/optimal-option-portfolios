"""Optimization problems P1, P2, P3 from Section 3."""

import math

import numpy as np
from scipy.optimize import minimize
from scipy.optimize import minimize_scalar
from scipy.stats import norm

from oop.risk import cfvar2
from oop.risk import cfvar3
from oop.types import FloatArray


def solve_variance_minimization(v: FloatArray, q_matrix: FloatArray) -> FloatArray:
    """Closed form Eq. (4) for P1."""
    q_inv = np.linalg.inv(q_matrix)
    denom = float(v.T @ q_inv @ v)
    return (q_inv @ v) / denom


def compute_epsilon_star(alpha: float, u: FloatArray, v: FloatArray, q_matrix: FloatArray) -> float:
    """Computes epsilon_star using Appendix B derivation.

    Preferred path: closed-form roots from Appendix B.
    Deterministic fallback: bounded numerical minimization if root conditions fail.
    """
    z = float(norm.ppf(alpha))
    if not np.isfinite(z):
        raise ValueError("Could not compute normal quantile")

    q_inv = np.linalg.inv(q_matrix)
    j_matrix = np.vstack([u.T, v.T])
    g_matrix = q_inv @ j_matrix.T @ np.linalg.inv(j_matrix @ q_inv @ j_matrix.T)

    g1 = g_matrix[:, 0]
    g2 = g_matrix[:, 1]
    a_scr = 0.5 * float(g1.T @ q_matrix @ g1)
    b_scr = float(g2.T @ q_matrix @ g1)
    c_scr = 0.5 * float(g2.T @ q_matrix @ g2)

    def variance_term(epsilon: float) -> float:
        return a_scr * epsilon * epsilon + b_scr * epsilon + c_scr

    def objective(epsilon: float) -> float:
        term = variance_term(epsilon)
        if term <= 0.0:
            return float("inf")
        return -epsilon - z * math.sqrt(term)

    a_cal = 4.0 * a_scr * a_scr * z * z - 4.0 * a_scr
    b_cal = 4.0 * a_scr * b_scr * z * z - 4.0 * b_scr
    c_cal = b_scr * b_scr * z * z - 4.0 * c_scr
    discriminant = b_cal * b_cal - 4.0 * a_cal * c_cal

    candidates = []
    if abs(a_cal) > 1e-12 and discriminant >= 0.0:
        eps_plus = (-b_cal + math.sqrt(discriminant)) / (2.0 * a_cal)
        eps_minus = (-b_cal - math.sqrt(discriminant)) / (2.0 * a_cal)
        if 2.0 * a_scr * eps_plus + b_scr > 0.0 and variance_term(eps_plus) > 0.0:
            candidates.append(eps_plus)
        if 2.0 * a_scr * eps_minus + b_scr > 0.0 and variance_term(eps_minus) > 0.0:
            candidates.append(eps_minus)

    if candidates:
        return min(candidates, key=objective)

    # Deterministic fallback for synthetic/invalid input regimes.
    search_radius = 1e3
    result = minimize_scalar(objective, method="bounded", bounds=(-search_radius, search_radius))
    if not result.success or not np.isfinite(result.fun):
        raise ValueError("Could not compute epsilon_star via closed-form or fallback solver")
    return float(result.x)


def solve_cfvar2_closed_form(
    q_matrix: FloatArray,
    u: FloatArray,
    v: FloatArray,
    alpha: float,
) -> FloatArray:
    """Eq. (5)-(6) for P2 with determined epsilon_star."""
    epsilon_star = compute_epsilon_star(alpha=alpha, u=u, v=v, q_matrix=q_matrix)
    q_inv = np.linalg.inv(q_matrix)
    j_matrix = np.vstack([u.T, v.T])
    psi_star = np.array([epsilon_star, 1.0], dtype=float)
    left = q_inv @ j_matrix.T
    right = np.linalg.inv(j_matrix @ q_inv @ j_matrix.T) @ psi_star
    return left @ right


def solve_cfvar3_numerical(
    v: FloatArray,
    initial_x: FloatArray,
    objective_callable,
) -> FloatArray:
    """Numerical solution for P3 with equality constraint x^T v = 1."""
    constraints = [{"type": "eq", "fun": lambda x: float(np.dot(x, v) - 1.0)}]
    result = minimize(objective_callable, x0=initial_x, method="SLSQP", constraints=constraints)
    if not result.success:
        raise RuntimeError(f"Optimization failed: {result.message}")
    return np.asarray(result.x, dtype=float)


def build_cfvar3_objective(alpha: float, u: FloatArray, q_matrix: FloatArray, kappa3_fn):
    """Factory for numerical P3 objective."""

    def objective(x: FloatArray) -> float:
        return cfvar3(alpha, u, q_matrix, np.asarray(x, dtype=float), float(kappa3_fn(x)))

    return objective


def compare_cfvar2_solution_quality(alpha: float, u: FloatArray, v: FloatArray, q_matrix: FloatArray) -> float:
    """Returns CFVaR2 value at closed-form solution for sanity checks."""
    x_star = solve_cfvar2_closed_form(q_matrix=q_matrix, u=u, v=v, alpha=alpha)
    return cfvar2(alpha=alpha, u=u, q_matrix=q_matrix, x=x_star)
