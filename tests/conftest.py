import pytest
from playwright.sync_api import Page

from pages.cashier_login_page import CashierLoginPage
from utils.cashier_auth import ensure_cashier_running
from utils.config import Config


@pytest.fixture(scope="session", autouse=True)
def _ensure_cashier_running() -> None:
  ensure_cashier_running(Config.CASHIER_BASE_URL)


@pytest.fixture(scope="session")
def browser_type_launch_args() -> dict:
  # 使用本机已安装的 Chrome，无需 playwright install chromium
  return {
    "headless": Config.HEADLESS,
    "channel": Config.BROWSER_CHANNEL,
  }


@pytest.fixture
def cashier_login_page(page: Page) -> CashierLoginPage:
  page.set_default_timeout(Config.ACTION_TIMEOUT)
  page.set_default_navigation_timeout(Config.NAVIGATION_TIMEOUT)
  return CashierLoginPage(page, Config.CASHIER_BASE_URL)
