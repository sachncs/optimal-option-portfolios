# Research Determination Notes

## Overview

This document tracks the determination status of various parameters and quantities from the paper [arXiv:2601.07991v2](https://arxiv.org/abs/2601.07991v2).

## Status Legend

- **DETERMINED** — Quantity has been verified and implemented
- **ASSUMPTION** — Implementation based on reasonable assumption
- **NOT DETERMINED** — Quantity not fully resolved
- **UNKNOWN** — Status unknown

## Parameters

### c (Scalar from Eq. 3)

**Status**: DETERMINED

**Source**: Section 2.4, extracted from HTML

**Implementation**: `moments.py`

### h (Vector from Eq. 3)

**Status**: DETERMINED

**Source**: Section 2.4, extracted from HTML

**Implementation**: `moments.py`

### q (Quadratic Form from Eq. 3)

**Status**: DETERMINED

**Source**: Section 2.4, extracted from HTML

**Implementation**: `reproduction_math.py`

### H (Matrix from Eq. 3)

**Status**: DETERMINED

**Source**: Section 2.4, extracted from HTML

**Implementation**: `moments.py`

### E (Matrix from Eq. 3)

**Status**: DETERMINED

**Source**: Section 2.4, extracted from HTML

**Implementation**: `moments.py`

### epsilon_star (Appendix B)

**Status**: DETERMINED

**Source**: Appendix B derivation

**Implementation**: `optimization.py`

## Algorithm Parameters

### alpha (Risk Parameter)

**Status**: DETERMINED

**Source**: Section 4.1

**Constraint**: 0 < alpha < 0.5

**Default**: 0.05

### nu (Degrees of Freedom)

**Status**: ASSUMPTION

**Source**: Section 4.2

**Constraint**: nu > 6 (configurable)

**Implementation**: Enforced via `enforce_nu_greater_than_six` config option

### method (Optimization Method)

**Status**: DETERMINED

**Source**: Section 4

**Options**: `all`, `variance`, `cfvar2`, `cfvar3`

## Implementation Notes

### Variance-Consistent Q Reconstruction

**Status**: DETERMINED

The Q matrix reconstruction uses variance-consistent formulation for exact quadratic behavior.

### Deterministic Seed Control

**Status**: DETERMINED

All random operations are seeded for reproducibility via `np.random.default_rng(seed)`.

## Open Questions

1. Optimal solver tolerances for different portfolio sizes
2. Parallelization strategy for large-scale problems
3. GPU acceleration feasibility

## References

- [arXiv:2601.07991v2](https://arxiv.org/abs/2601.07991v2) — Main paper
- [R `sn` package](https://CRAN.R-project.org/package=sn) — Reference implementation for statistical estimators
