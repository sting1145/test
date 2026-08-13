import json
import os
import sys
from datetime import datetime
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from utils.config import Config
from utils.report_paths import get_screenshot_dir

DEFAULT_ALLURE_CONFIG = {
  "reportName": "熊猫掌柜收银台-UI自动化测试报告",
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
  allure_results = os.getenv("ALLURE_RESULTS_DIR")
  if not allure_results:
    return

  root = Path(__file__).parent
  results_dir = Path(allure_results)
  results_dir.mkdir(parents=True, exist_ok=True)
  allure_config = _load_allure_config(root)

  (results_dir / "executor.json").write_text(
    json.dumps(
      {
        "name": "pytest",
        "type": "local",
        "reportName": allure_config["reportName"],
        "buildName": "收银台本地执行",
      },
      ensure_ascii=False,
    ),
    encoding="utf-8",
  )

  (results_dir / "environment.properties").write_text(
    "\n".join(
      [
        f"CASHIER_BASE_URL={Config.CASHIER_BASE_URL}",
        f"CASHIER_SERVER_IP={Config.CASHIER_SERVER_IP}",
        f"Python={sys.version.split()[0]}",
        "Framework=pytest + Playwright + Allure",
        "Project=ui-automation-cashier",
        f"ReportLanguage={allure_config['lang']}",
        f"ReportName={allure_config['reportName']}",
      ]
    ),
    encoding="utf-8",
  )


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
  outcome = yield
  report = outcome.get_result()
  setattr(item, f"rep_{report.when}", report)

  if report.when not in ("setup", "call") or not report.failed:
    return

  page: Page | None = item.funcargs.get("page")
  if not page:
    return

  screenshot_dir = get_screenshot_dir()
  screenshot_dir.mkdir(parents=True, exist_ok=True)
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  screenshot_path = screenshot_dir / f"failure_{report.when}_{item.name}_{timestamp}.png"

  try:
    png_bytes = page.screenshot(full_page=True)
    screenshot_path.write_bytes(png_bytes)
    allure.attach(
      png_bytes,
      name=f"失败截图 ({report.when})",
      attachment_type=allure.attachment_type.PNG,
      extension="png",
    )
  except Exception:
    pass
