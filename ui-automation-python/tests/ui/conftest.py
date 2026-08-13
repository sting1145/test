import os
from datetime import datetime

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.login_page import LoginPage
from pages.password_reset_page import PasswordResetPage
from utils.config import Config


@pytest.fixture(scope="session")
def base_url() -> str:
  return Config.BASE_URL


@pytest.fixture(scope="session")
def driver():
  """整个 UI 测试会话共用一个浏览器。"""
  options = Options()
  if Config.HEADLESS:
    options.add_argument("--headless=new")
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--window-size=1920,1080")
  options.add_argument("--lang=zh-CN")

  browser = webdriver.Chrome(options=options)
  browser.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)

  yield browser

  browser.quit()


@pytest.fixture(autouse=True)
def _cleanup_after_test(driver):
  yield
  handles = driver.window_handles
  if len(handles) > 1:
    main = handles[0]
    for handle in handles[1:]:
      driver.switch_to.window(handle)
      driver.close()
    driver.switch_to.window(main)

  try:
    driver.execute_script(
      """
      document.querySelectorAll('.el-message-box__wrapper').forEach(el => {
        if (el.style.display !== 'none') {
          const btn = el.querySelector('button.el-button--primary');
          if (btn) btn.click();
        }
      });
      """
    )
  except Exception:
    pass


@pytest.fixture
def login_page(driver, base_url) -> LoginPage:
  return LoginPage(driver, base_url, Config.EXPLICIT_WAIT)


@pytest.fixture
def password_reset_page(driver, base_url) -> PasswordResetPage:
  return PasswordResetPage(driver, base_url, Config.EXPLICIT_WAIT)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
  outcome = yield
  report = outcome.get_result()
  setattr(item, f"rep_{report.when}", report)

  if report.when not in ("setup", "call") or not report.failed:
    return

  driver = item.funcargs.get("driver")
  if not driver:
    return

  try:
    png_bytes = driver.get_screenshot_as_png()
  except Exception:
    return

  run_id = os.getenv("CURRENT_RUN_ID", "unknown")
  screenshot_dir = Config.SCREENSHOT_DIR / run_id
  screenshot_dir.mkdir(parents=True, exist_ok=True)
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  screenshot_path = screenshot_dir / f"failure_{report.when}_{item.name}_{timestamp}.png"

  try:
    screenshot_path.write_bytes(png_bytes)
  except Exception:
    pass

  allure.attach(
    png_bytes,
    name=f"失败截图 ({report.when})",
    attachment_type=allure.attachment_type.PNG,
    extension="png",
  )
