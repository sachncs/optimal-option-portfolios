import json
from pathlib import Path

import pytest

from oop.config import load_config
from oop.config import validate_config


def test_load_config_defaults() -> None:
    config = load_config(None)
    assert config.optimization.alpha == 0.05


def test_validate_config_rejects_invalid_alpha() -> None:
    config = load_config(None)
    payload = {
        "runtime": {
            "seed": config.runtime.seed,
            "log_level": config.runtime.log_level,
            "output_dir": config.runtime.output_dir,
        },
        "optimization": {
            "alpha": 0.6,
            "method": config.optimization.method,
            "enforce_nu_greater_than_six": config.optimization.enforce_nu_greater_than_six,
        },
    }
    path = Path("/tmp/oop_bad_config.json")
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError):
        validate_config(load_config(str(path)))
