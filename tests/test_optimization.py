import numpy as np

from oop.optimization import solve_cfvar2_closed_form
from oop.optimization import solve_cfvar3_numerical
from oop.optimization import solve_variance_minimization


def test_variance_solution_satisfies_budget_constraint() -> None:
    q = np.array([[2.0, 0.1], [0.1, 1.5]])
    v = np.array([1.2, 0.8])
    x = solve_variance_minimization(v, q)
    assert np.isclose(float(x.T @ v), 1.0, atol=1e-8)


def test_cfvar2_closed_form_satisfies_affine_constraint() -> None:
    q = np.array([[2.5, 0.0], [0.0, 1.5]])
    u = np.array([0.1, 0.3])
    v = np.array([1.0, 2.0])
    x = solve_cfvar2_closed_form(q_matrix=q, u=u, v=v, alpha=0.05)
    assert np.isclose(float(x.T @ v), 1.0, atol=1e-8)


def test_cfvar3_numerical_enforces_budget_constraint() -> None:
    v = np.array([1.0, 2.0, 1.5])

    def objective(x: np.ndarray) -> float:
        return float(np.sum(x**2))

    x0 = np.ones(3) / 3.0
    x = solve_cfvar3_numerical(v=v, initial_x=x0, objective_callable=objective)
    assert np.isclose(float(x.T @ v), 1.0, atol=1e-6)
