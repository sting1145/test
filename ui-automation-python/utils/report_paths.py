import os
from pathlib import Path


def get_allure_results_dir() -> Path:
  custom = os.getenv("ALLURE_RESULTS_DIR")
  if custom:
    return Path(custom)
  return Path(__file__).parent.parent / "allure-results"


def get_reports_root() -> Path:
  return Path(__file__).parent.parent / "reports"


def get_runs_root() -> Path:
  return get_reports_root() / "runs"
