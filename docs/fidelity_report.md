# Fidelity Report

## Overview

This document describes the fidelity of the implementation to the reference paper [arXiv:2601.07991v2](https://arxiv.org/abs/2601.07991v2).

## Paper Fidelity

### Variance Minimization (Section 2.1)

**Status**: Fully Implemented

The minimum variance portfolio optimization under budget constraint is implemented as:

```
minimize    x^T Q x
subject to  x^T v = 1
```

**Implementation**: `solve_variance_minimization` in `optimization.py`

### CFVaR2 Closed-Form (Section 4.2)

**Status**: Fully Implemented

The closed-form solution for CFVaR2 optimization is implemented analytically.

**Implementation**: `solve_cfvar2_closed_form` in `optimization.py`

### CFVaR3 Numerical (Section 4.3)

**Status**: Fully Implemented

Third-order risk measure optimization via numerical methods.

**Implementation**: `solve_cfvar3_numerical` in `optimization.py`

## Parameter Definitions

### c (Eq. 3)

**Status**: Implemented

The scalar `c` from the moment expansion is computed in `moments.py` and `reproduction_math.py`.

### h (Eq. 3)

**Status**: Implemented

The vector `h` from the moment expansion is computed in `moments.py`.

### q (Eq. 3)

**Status**: Implemented

The quadratic form `q` is computed using variance-consistent reconstruction.

### epsilon_star (Appendix B)

**Status**: Implemented

The optimal `epsilon_star` scalar is computed from the Appendix B derivation.

## Mismatches and Caveats

### Synthetic Data

**Status**: ASSUMPTION

The pipeline uses synthetic data for demonstration. Real-market replication requires data-specific integration.

### Numerical Precision

**Status**: ASSUMPTION

Numerical optimization may have slight variations across platforms due to floating-point arithmetic.

### Estimator Parity with R `sn`

**Status**: NOT DETERMINED

Some statistical estimators may differ from R's `sn` package implementations.

## Testing Coverage

All implemented algorithms are covered by unit tests in `tests/`:

- `test_optimization.py` — Solver correctness
- `test_risk.py` — Risk measure calculations
- `test_config.py` — Configuration validation
- `test_determinism.py` — Reproducibility verification
- `test_determined_quantities.py` — Parameter computation
