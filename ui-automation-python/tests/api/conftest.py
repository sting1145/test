import json

import allure
import pytest

from api.clients.passport_client import PassportClient
from utils.config import Config


def _require_session_cookie() -> str:
  cookie = Config.SESSION_COOKIE_B.strip()
  if not cookie:
    pytest.skip("未配置 SESSION_COOKIE_B，请人工登录后把 Cookie 写入 .env")
  return cookie


def _apply_api_headers(client: PassportClient) -> None:
  if Config.API_REFERER.strip():
    client.set_referer(Config.API_REFERER.strip())


@pytest.fixture
def passport_client() -> PassportClient:
  client = PassportClient(Config.BASE_URL, timeout=Config.API_TIMEOUT)
  client.warm_session()
  return client


@pytest.fixture
def authenticated_client() -> PassportClient:
  client = PassportClient(Config.API_BASE_URL, timeout=Config.API_TIMEOUT)
  client.load_cookie_header(_require_session_cookie())
  _apply_api_headers(client)
  return client


@pytest.fixture
def anonymous_client() -> PassportClient:
  client = PassportClient(Config.API_BASE_URL, timeout=Config.API_TIMEOUT)
  _apply_api_headers(client)
  return client


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
  outcome = yield
  report = outcome.get_result()

  if report.when != "call" or not report.failed:
    return

  for fixture_name in ("passport_client", "authenticated_client", "anonymous_client"):
    client = item.funcargs.get(fixture_name)
    if not client:
      continue

    last = getattr(client, "_last_response", None)
    if not last:
      continue

    allure.attach(
      json.dumps(
        {
          "status_code": last.status_code,
          "body": last.text[:4000],
        },
        ensure_ascii=False,
        indent=2,
      ),
      name="最后一次接口响应",
      attachment_type=allure.attachment_type.JSON,
      extension="json",
    )
    break
