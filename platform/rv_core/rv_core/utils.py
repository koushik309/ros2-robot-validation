import os
import shutil
from datetime import datetime
from pathlib import Path

def create_run_dir(base_dir: str = "artifacts") -> Path:
    """Create a timestamped directory for the current test run."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path(base_dir) / f"run_{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir

def save_spec_copy(spec_dict: dict, run_dir: Path):
    """Save a copy of the original spec YAML in the run directory."""
    import yaml
    spec_path = run_dir / "spec.yaml"
    with open(spec_path, 'w') as f:
        yaml.dump(spec_dict, f)
    return spec_path