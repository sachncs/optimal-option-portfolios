"""Production execution pipeline for reproducible optimization runs."""

from dataclasses import asdict
import json
from pathlib import Path

import numpy as np

from oop.config import ExperimentConfig
from oop.optimization import build_cfvar3_objective
from oop.optimization import solve_cfvar2_closed_form
from oop.optimization import solve_cfvar3_numerical
from oop.optimization import solve_variance_minimization
from oop.risk import cfvar2


def run_reproduction(config: ExperimentConfig) -> dict[str, object]:
    """Runs end-to-end optimization and returns structured outputs.

    Uses synthetic matrices as a self-contained production smoke pipeline.
    External data ingestion is project-dependent and plugin users can replace this stage.
    """
    rng = np.random.default_rng(config.runtime.seed)
    instrument_count = 5
    random_matrix = rng.normal(size=(instrument_count, instrument_count))
    q_matrix = random_matrix.T @ random_matrix + 0.5 * np.eye(instrument_count)
    v = np.abs(rng.normal(size=instrument_count)) + 0.1
    u = rng.normal(size=instrument_count)

    variance_solution = solve_variance_minimization(v, q_matrix)
    cfvar2_solution = solve_cfvar2_closed_form(
        q_matrix=q_matrix,
        u=u,
        v=v,
        alpha=config.optimization.alpha,
    )

    def mock_kappa3(vector_x: np.ndarray) -> float:
        return float(0.01 * np.sum(vector_x**3))

    objective = build_cfvar3_objective(
        alpha=config.optimization.alpha,
        u=u,
        q_matrix=q_matrix,
        kappa3_fn=mock_kappa3,
    )
    initial_x = np.ones(instrument_count) / np.sum(v)
    cfvar3_solution = solve_cfvar3_numerical(v=v, initial_x=initial_x, objective_callable=objective)

    return {
        "config": asdict(config),
        "inputs": {
            "u": u.tolist(),
            "v": v.tolist(),
            "q_matrix": q_matrix.tolist(),
        },
        "outputs": {
            "variance_solution": variance_solution.tolist(),
            "cfvar2_solution": cfvar2_solution.tolist(),
            "cfvar3_solution": cfvar3_solution.tolist(),
            "cfvar2_at_variance_solution": cfvar2(
                config.optimization.alpha,
                u,
                q_matrix,
                variance_solution,
            ),
        },
        "uncertainty": {
            "status": "ASSUMPTION",
            "items": [
                "Pipeline demo uses synthetic inputs; real-market replication requires data-specific integration.",
            ],
        },
    }


def save_report(report: dict[str, object], output_dir: str) -> Path:
    """Persists JSON report for reproducibility and downstream systems."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    report_path = output_path / "reproduction_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report_path
