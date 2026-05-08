# Changelog

## [0.2.1] - 2026-05-09
### Added
- CI workflow with lint, type-check, tests, build, and wheel smoke test.
- Deterministic validation capability for reproducibility checks.
- Research determination notes for `c`, `h`, `q`, and `epsilon_star`.

### Changed
- CFVaR2 closed-form solver now computes `epsilon_star` from Appendix-B derivation.
- Reproduction math now uses variance-consistent `Q` reconstruction for exact quadratic behavior.

## [0.2.0] - 2026-05-09
### Added
- Production package rename to `oop`.
- Public API, CLI, config, logging, pipeline, tests, and docs.
