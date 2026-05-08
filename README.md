# oop

Production-ready Python package for optimal option portfolio optimization, based on arXiv:2601.07991v2.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Package Usage

```python
import numpy as np
from oop import solve_variance_minimization

q_matrix = np.array([[2.0, 0.1], [0.1, 1.5]])
v = np.array([1.2, 0.8])
weights = solve_variance_minimization(v=v, q_matrix=q_matrix)
print(weights)
```

## CLI Usage

```bash
oop --command reproduce-report
oop --command print-report
oop --command validate-determinism --repetitions 3
oop --config config.json --command reproduce-report
```

Default artifact output: `artifacts/reproduction_report.json`

## Config Format

```json
{
  "runtime": {
    "seed": 7,
    "log_level": "INFO",
    "output_dir": "artifacts"
  },
  "optimization": {
    "alpha": 0.05,
    "method": "all",
    "enforce_nu_greater_than_six": true
  }
}
```

## Deterministic Behavior

- For fixed config and seed, `run_reproduction` is deterministic.
- `oop --command validate-determinism` asserts deterministic repeatability.
- Remaining approximation caveats (e.g., estimator parity with R `sn`) are deterministic in this package baseline: fixed-input behavior is reproducible and test-covered.

## Production Characteristics

- Typed public API for integration into external systems.
- Deterministic seed-controlled execution.
- Structured JSON outputs for downstream orchestration.
- Validation and defensive checks on inputs.
- Separation of faithful baseline and mismatch documentation.

## Quality Gates

```bash
PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -q
python -m mypy src/oop
python -m ruff check src tests scripts
python -m build
```

## Fidelity and Mismatches

- [Fidelity report](docs/fidelity_report.md)
- [Mismatch report](docs/mismatch_report.md)
- [Determination notes](docs/research_determination.md)
- [Release process](docs/release.md)

Missing details are explicitly marked where relevant:
- `NOT DETERMINED`
- `ASSUMPTION`
- `UNKNOWN`
