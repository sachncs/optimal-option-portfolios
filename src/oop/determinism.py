"""Determinism checks for production reproducibility."""

import json

from oop.config import ExperimentConfig
from oop.pipeline import run_reproduction


def deterministic_report(config: ExperimentConfig, repetitions: int = 2) -> dict[str, object]:
    """Runs repeated reports and asserts deterministic equality.

    Args:
      config: Runtime and optimization configuration.
      repetitions: Number of repeated runs.

    Returns:
      A summary dictionary including pass/fail and first report.
    """
    if repetitions < 2:
        raise ValueError("repetitions must be >= 2")

    serialized = []
    reports = []
    for _ in range(repetitions):
        report = run_reproduction(config)
        reports.append(report)
        serialized.append(json.dumps(report, sort_keys=True))

    is_equal = all(item == serialized[0] for item in serialized[1:])
    return {
        "deterministic": is_equal,
        "repetitions": repetitions,
        "seed": config.runtime.seed,
        "reference_report": reports[0],
    }
