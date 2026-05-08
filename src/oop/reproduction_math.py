"""Paper-faithful algebraic constructions for Section 2.4."""

import numpy as np

from oop.moments import compute_c_scalar
from oop.moments import compute_e_matrix
from oop.moments import compute_h_matrix
from oop.moments import compute_h_vector
from oop.moments import compute_q_vector
from oop.types import FloatArray


def portfolio_greeks_from_shares(
    x: FloatArray,
    theta_vector: FloatArray,
    d_matrix: FloatArray,
    gamma_tensor: FloatArray,
) -> tuple[float, FloatArray, FloatArray]:
    """Computes theta, delta, gamma for a portfolio of options."""
    theta_value = float(theta_vector.T @ x)
    delta_vector = d_matrix @ x
    gamma_matrix = np.einsum("m,mij->ij", x, gamma_tensor)
    return theta_value, delta_vector, gamma_matrix


def variance_direct_formula(
    gamma_matrix: FloatArray,
    delta_vector: FloatArray,
    mu: FloatArray,
    sigma: FloatArray,
    nu: float,
    c_scalar: float,
    h_vector: FloatArray,
) -> float:
    """Direct scalar variance formula from Section 2.4."""
    a_vector = gamma_matrix @ mu + delta_vector
    term1 = (nu**2 / (2.0 * (nu - 2.0) * (nu - 4.0))) * np.trace((gamma_matrix @ sigma) @ (gamma_matrix @ sigma))
    term2 = (nu**2 / (2.0 * (nu - 2.0) ** 2 * (nu - 4.0))) * (np.trace(gamma_matrix @ sigma) ** 2)
    term3 = (nu / (nu - 2.0)) * float(a_vector.T @ sigma @ a_vector)
    term4 = (2.0 * c_scalar * nu / (nu - 3.0)) * float(a_vector.T @ sigma @ gamma_matrix @ h_vector)
    term5 = (c_scalar * nu / ((nu - 2.0) * (nu - 3.0))) * float(a_vector.T @ h_vector) * float(np.trace(gamma_matrix @ sigma))
    term6 = -(c_scalar * nu / (nu - 3.0)) * float(a_vector.T @ h_vector) * float(h_vector.T @ gamma_matrix @ h_vector)
    term7 = -(c_scalar**2) * (float(a_vector.T @ h_vector) ** 2)
    return float(term1 + term2 + term3 + term4 + term5 + term6 + term7)


def build_linearized_matrices(
    theta_vector: FloatArray,
    d_matrix: FloatArray,
    gamma_tensor: FloatArray,
    mu: FloatArray,
    sigma: FloatArray,
    nu: float,
    omega: FloatArray,
    delta_t: float,
) -> tuple[FloatArray, FloatArray]:
    """Builds u and Q using determined c,h,q,H,E definitions."""
    m = gamma_tensor.shape[0]
    c_scalar = compute_c_scalar(nu)
    h_vector = compute_h_vector(sigma=sigma, omega=omega)

    p_vector = np.array([np.trace(gamma_tensor[idx] @ sigma) for idx in range(m)], dtype=float)
    b_matrix = np.vstack([mu.T @ gamma_tensor[idx] for idx in range(m)])
    xi_vector = np.array([0.5 * float(mu.T @ gamma_tensor[idx] @ mu) for idx in range(m)], dtype=float)

    zeta = delta_t * theta_vector + d_matrix.T @ mu + (nu / (2.0 * (nu - 2.0))) * p_vector + xi_vector
    u_vector = zeta + c_scalar * b_matrix @ h_vector + c_scalar * d_matrix.T @ h_vector

    r_matrix = np.zeros((m, m), dtype=float)
    for i in range(m):
        for j in range(m):
            r_matrix[i, j] = float(np.trace(gamma_tensor[i] @ sigma @ gamma_tensor[j] @ sigma))

    u_matrix = (
        (2.0 * nu / (nu - 2.0)) * ((d_matrix.T + b_matrix) @ sigma @ (d_matrix.T + b_matrix).T)
        + (nu**2 / ((nu - 2.0) * (nu - 4.0))) * r_matrix
        + (nu**2 / ((nu - 2.0) ** 2 * (nu - 4.0))) * np.outer(p_vector, p_vector)
    )

    q_vector = compute_q_vector(gamma_tensor=gamma_tensor, h_vector=h_vector)
    h_matrix = compute_h_matrix(d_matrix=d_matrix, b_matrix=b_matrix, sigma=sigma, gamma_tensor=gamma_tensor, h_vector=h_vector)
    e_matrix = compute_e_matrix(d_matrix=d_matrix, b_matrix=b_matrix, sigma=sigma, gamma_tensor=gamma_tensor, h_vector=h_vector)

    b_plus_dt = b_matrix + d_matrix.T
    q_tilde = (
        u_matrix
        + (4.0 * c_scalar * nu / (nu - 3.0)) * (h_matrix + e_matrix)
        + (2.0 * c_scalar * nu / ((nu - 2.0) * (nu - 3.0))) * np.outer(b_plus_dt @ h_vector, p_vector)
        - (2.0 * c_scalar * nu / (nu - 3.0)) * np.outer(b_plus_dt @ h_vector, q_vector)
        - 2.0 * c_scalar**2 * np.outer(b_plus_dt @ h_vector, b_plus_dt @ h_vector)
    )

    q_matrix = 0.5 * (q_tilde + q_tilde.T)
    return u_vector, q_matrix


def reconstruct_q_matrix_from_direct_variance(
    theta_vector: FloatArray,
    d_matrix: FloatArray,
    gamma_tensor: FloatArray,
    mu: FloatArray,
    sigma: FloatArray,
    nu: float,
    omega: FloatArray,
) -> FloatArray:
    """Reconstructs Q from direct variance formula evaluations.

    Since Var[ΔV(x)] is quadratic in x, this recovers the exact symmetric Q.
    """
    m = gamma_tensor.shape[0]
    c_scalar = compute_c_scalar(nu)
    h_vector = compute_h_vector(sigma=sigma, omega=omega)
    q_matrix = np.zeros((m, m), dtype=float)

    def variance_at(x_vec: FloatArray) -> float:
        _, delta_vec, gamma_mat = portfolio_greeks_from_shares(
            x=x_vec,
            theta_vector=theta_vector,
            d_matrix=d_matrix,
            gamma_tensor=gamma_tensor,
        )
        return variance_direct_formula(
            gamma_matrix=gamma_mat,
            delta_vector=delta_vec,
            mu=mu,
            sigma=sigma,
            nu=nu,
            c_scalar=c_scalar,
            h_vector=h_vector,
        )

    basis = np.eye(m)
    for i in range(m):
        q_matrix[i, i] = 2.0 * variance_at(basis[i])
    for i in range(m):
        for j in range(i + 1, m):
            mixed = variance_at(basis[i] + basis[j])
            q_matrix[i, j] = mixed - 0.5 * q_matrix[i, i] - 0.5 * q_matrix[j, j]
            q_matrix[j, i] = q_matrix[i, j]
    return q_matrix
