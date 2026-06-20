# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

### Changed
- Migrated to production-ready package structure.

## [0.0.1] - 2026-05-09

### Added
- Initial release with core optimization algorithms.
- Variance minimization solver.
- CFVaR2 closed-form solver.
- CFVaR3 numerical solver.

[Unreleased]: https://github.com/sachin/optimal-option-portfolios/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/sachin/optimal-option-portfolios/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/sachin/optimal-option-portfolios/compare/v0.0.1...v0.2.0
[0.0.1]: https://github.com/sachin/optimal-option-portfolios/releases/tag/v0.0.1
