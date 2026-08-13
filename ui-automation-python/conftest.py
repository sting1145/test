import json
import os
import sys
from pathlib import Path

import pytest

from utils.config import Config
from utils.report_paths import get_allure_results_dir

DEFAULT_ALLURE_CONFIG = {
  "reportName": "熊猫掌柜 自动化测试报告",
  "lang": "zh",
}


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
  allure_dir = config.getoption("--alluredir", default=None)
  if allure_dir:
    os.environ["ALLURE_RESULTS_DIR"] = str(Path(allure_dir).resolve())


def _load_allure_config(root: Path) -> dict:
  config_path = root / "config" / "allure.json"
  if not config_path.exists():
    return DEFAULT_ALLURE_CONFIG.copy()
  try:
    return json.loads(config_path.read_text(encoding="utf-8"))
  except (json.JSONDecodeError, OSError):
    return DEFAULT_ALLURE_CONFIG.copy()


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
  if not os.getenv("ALLURE_RESULTS_DIR"):
    return

  root = Path(__file__).parent
  allure_results = get_allure_results_dir()
  allure_results.mkdir(parents=True, exist_ok=True)
  allure_config = _load_allure_config(root)
  suite = os.getenv("TEST_SUITE", "automation")

  executor_file = allure_results / "executor.json"
  executor_file.write_text(
    json.dumps(
      {
        "name": "pytest",
        "type": "local",
        "reportName": allure_config["reportName"],
        "buildName": f"本地执行-{suite}",
      },
      ensure_ascii=False,
    ),
    encoding="utf-8",
  )

  env_file = allure_results / "environment.properties"
  env_file.write_text(
    "\n".join(
      [
        f"BASE_URL={Config.BASE_URL}",
        f"Python={sys.version.split()[0]}",
        f"TEST_SUITE={suite}",
        "Framework=pytest + Allure",
        "Project=ui-automation-python",
        f"ReportLanguage={allure_config['lang']}",
        f"ReportName={allure_config['reportName']}",
      ]
    ),
    encoding="utf-8",
  )

  categories_src = root / "config" / "categories.json"
  if categories_src.exists():
    (allure_results / "categories.json").write_text(
      categories_src.read_text(encoding="utf-8"),
      encoding="utf-8",
    )
