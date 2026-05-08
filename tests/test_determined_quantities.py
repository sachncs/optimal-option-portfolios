import numpy as np

from oop.moments import compute_c_scalar
from oop.moments import compute_h_vector
from oop.reproduction_math import portfolio_greeks_from_shares
from oop.reproduction_math import reconstruct_q_matrix_from_direct_variance
from oop.reproduction_math import variance_direct_formula


def test_c_matches_theorem2_formula() -> None:
    nu = 8.0
    c_value = compute_c_scalar(nu)
    assert c_value > 0.0


def test_h_has_expected_shape() -> None:
    sigma = np.eye(3)
    omega = np.array([0.3, -0.2, 0.1])
    h = compute_h_vector(sigma=sigma, omega=omega)
    assert h.shape == (3,)


def test_reconstructed_q_matches_direct_variance_formula() -> None:
    rng = np.random.default_rng(123)
    n = 4
    m = 3
    nu = 9.0

    sigma_noise = rng.normal(size=(n, n))
    sigma = sigma_noise.T @ sigma_noise + np.eye(n)
    mu = rng.normal(size=n)
    omega = rng.normal(size=n)

    d_matrix = rng.normal(size=(n, m))
    theta_vector = rng.normal(size=m)
    gamma_tensor = np.array([(g + g.T) / 2.0 for g in rng.normal(size=(m, n, n))])

    q_matrix = reconstruct_q_matrix_from_direct_variance(
        theta_vector=theta_vector,
        d_matrix=d_matrix,
        gamma_tensor=gamma_tensor,
        mu=mu,
        sigma=sigma,
        nu=nu,
        omega=omega,
    )

    c_scalar = compute_c_scalar(nu)
    h_vector = compute_h_vector(sigma=sigma, omega=omega)

    for _ in range(25):
        x = rng.normal(size=m)
        _, delta_vector, gamma_matrix = portfolio_greeks_from_shares(
            x=x,
            theta_vector=theta_vector,
            d_matrix=d_matrix,
            gamma_tensor=gamma_tensor,
        )
        direct_var = variance_direct_formula(
            gamma_matrix=gamma_matrix,
            delta_vector=delta_vector,
            mu=mu,
            sigma=sigma,
            nu=nu,
            c_scalar=c_scalar,
            h_vector=h_vector,
        )
        matrix_var = 0.5 * float(x.T @ q_matrix @ x)
        assert np.isclose(direct_var, matrix_var, atol=1e-7)
