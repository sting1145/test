from __future__ import annotations

import hashlib
import json
from typing import Any, Callable
from urllib.parse import urlparse

import requests
import websocket
from playwright.sync_api import Page

LOGIN_API_URL = "https://service.xiongmaozhanggui.com/1001/api/v1/backend/login"
DEFAULT_BAR_PORT = "16510"


def md5(value: str) -> str:
  return hashlib.md5(value.encode("utf-8")).hexdigest()


def ensure_cashier_running(base_url: str) -> None:
  login_url = f"{base_url.rstrip('/')}/html/login.html"
  try:
    response = requests.get(login_url, timeout=5)
  except requests.RequestException as exc:
    raise RuntimeError(
      f"收银台未就绪：无法连接 {base_url}，请先启动收银台程序"
    ) from exc

  if response.status_code >= 400:
    raise RuntimeError(f"收银台未就绪：{base_url} 返回 {response.status_code}")


def fetch_netbar_token(server_ip: str) -> dict[str, str]:
  ws_url = f"ws://{server_ip}:{DEFAULT_BAR_PORT}/async_app?app_id=1001&ip={server_ip}"
  connection = websocket.create_connection(ws_url, timeout=10)
  try:
    message = json.loads(connection.recv())
  finally:
    connection.close()

  data = message.get("data") or {}
  if not data.get("nid") or not data.get("token"):
    raise RuntimeError("WebSocket 未返回有效的 token/nid")

  return {"nid": data["nid"], "token": data["token"]}


def login_via_api(account: str, password: str, netbar_token: dict[str, str]) -> dict[str, Any]:
  body = login_via_api_raw(account, password, netbar_token)
  if body.get("status") != 200:
    raise RuntimeError(f"登录接口返回失败：{body.get('msg', body)}")

  return body


def login_via_api_raw(account: str, password: str, netbar_token: dict[str, str]) -> dict[str, Any]:
  payload = {
    "user_name": account,
    "password": md5(password),
    "token": netbar_token["token"],
    "nid": netbar_token["nid"],
  }
  response = requests.post(LOGIN_API_URL, json=payload, timeout=15)
  response.raise_for_status()
  return response.json()


def prepare_cashier_session(page: Page, server_ip: str, netbar_token: dict[str, str]) -> None:
  parsed = urlparse(page.url)
  http_port = parsed.port or "9981"
  page.evaluate(
    """
    ({ serverIp, netbarToken, httpPort }) => {
      localStorage.setItem('bar_ip', serverIp);
      localStorage.setItem('bar_port', '16510');
      localStorage.setItem('api_port', '9981');
      localStorage.setItem('ip', serverIp);
      localStorage.setItem('http_port', httpPort);
      localStorage.setItem('isNoLogin', 'true');
      localStorage.setItem('netbar', JSON.stringify(netbarToken));
    }
    """,
    {"serverIp": server_ip, "netbarToken": netbar_token, "httpPort": http_port},
  )


def mock_cashier_login_api(page: Page, login_response: dict[str, Any]) -> None:
  body = json.dumps(login_response, ensure_ascii=False)

  def handle(route):
    route.fulfill(status=200, content_type="application/json", body=body)

  page.route("**/api/v1/backend/login", handle)


def trigger_netbar_handshake(page: Page, netbar_token: dict[str, str]) -> None:
  page.evaluate(
    """
    (tokenData) => {
      if (typeof window.to_browser !== 'function') {
        throw new Error('登录页未初始化 to_browser，请确认收银台页面已加载完成');
      }
      window.to_browser(JSON.stringify({
        data: { type: 2, data: tokenData }
      }));
    }
    """,
    netbar_token,
  )


def read_stored_user_info(page: Page) -> dict[str, Any] | None:
  return page.evaluate(
    """
    () => {
      const raw = localStorage.getItem('userinfo');
      return raw ? JSON.parse(raw) : null;
    }
    """
  )


def perform_cashier_login(
  page: Page,
  *,
  server_ip: str,
  account: str,
  password: str,
  click_login: Callable[[], None] | None = None,
) -> dict[str, Any]:
  netbar_token = fetch_netbar_token(server_ip)
  login_response = login_via_api(account, password, netbar_token)
  return perform_cashier_login_with_response(
    page,
    server_ip=server_ip,
    netbar_token=netbar_token,
    login_response=login_response,
    click_login=click_login,
  )


def perform_cashier_login_with_response(
  page: Page,
  *,
  server_ip: str,
  netbar_token: dict[str, str],
  login_response: dict[str, Any],
  click_login: Callable[[], None] | None = None,
) -> dict[str, Any]:
  mock_cashier_login_api(page, login_response)
  prepare_cashier_session(page, server_ip, netbar_token)

  if click_login:
    click_login()
    page.wait_for_timeout(500)
    trigger_netbar_handshake(page, netbar_token)

  return login_response


def attempt_cashier_login(
  page: Page,
  *,
  server_ip: str,
  account: str,
  password: str,
  click_login: Callable[[], None] | None = None,
) -> dict[str, Any]:
  netbar_token = fetch_netbar_token(server_ip)
  login_response = login_via_api_raw(account, password, netbar_token)
  return perform_cashier_login_with_response(
    page,
    server_ip=server_ip,
    netbar_token=netbar_token,
    login_response=login_response,
    click_login=click_login,
  )
