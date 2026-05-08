import numpy as np
import pytest

from oop.risk import cfvar2
from oop.risk import cfvar3
from oop.risk import validate_shapes
from oop.risk import variance_quadratic


def test_validate_shapes_raises_on_incompatible_dims() -> None:
  u = np.ones(3)
  q = np.eye(4)
  x = np.ones(3)
  with pytest.raises(ValueError):
    validate_shapes(u, q, x)


def test_variance_quadratic_non_negative_for_psd_q() -> None:
  x = np.array([1.0, -2.0, 0.5])
  q = np.eye(3)
  assert variance_quadratic(q, x) >= 0.0


def test_cfvar3_reduces_to_cfvar2_when_kappa3_zero() -> None:
  u = np.array([0.2, -0.1, 0.3])
  q = np.array([[2.0, 0.1, 0.0], [0.1, 1.5, 0.2], [0.0, 0.2, 1.2]])
  x = np.array([0.5, 0.2, 0.1])
  assert np.isclose(cfvar2(0.05, u, q, x), cfvar3(0.05, u, q, x, 0.0), atol=1e-10)
