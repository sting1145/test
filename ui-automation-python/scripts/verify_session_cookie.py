"""校验 .env 中的 SESSION_COOKIE_B 是否可用。"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from api.clients.passport_client import PassportClient
from utils.api_session_assertions import assert_api_success
from utils.config import Config


def main() -> int:
  cookie = Config.SESSION_COOKIE_B.strip()
  if not cookie:
    print("未配置 SESSION_COOKIE_B")
    return 1

  client = PassportClient(Config.API_BASE_URL, timeout=Config.API_TIMEOUT)
  client.load_cookie_header(cookie)

  probe_path = Config.API_CURRENT_USER_PATH.strip() or Config.API_LIST_PATH.strip()
  if not probe_path:
    print("已加载 Cookie，但未配置 API_CURRENT_USER_PATH / API_LIST_PATH")
    print("请登录后在 Network 复制 current-user 和列表接口路径到 .env")
    return 0

  referer = Config.API_USER_REFERER if probe_path == Config.API_CURRENT_USER_PATH.strip() else Config.API_LIST_REFERER
  print(f"probe: GET {Config.API_BASE_URL}{probe_path}")
  response = client.get(probe_path, headers={"Referer": referer})
  print(f"status={response.status_code}")
  print(response.text[:500])

  try:
    assert_api_success(response, context=probe_path)
  except AssertionError as exc:
    print(f"FAIL: {exc}")
    return 2

  print("OK: Session Cookie 可用")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
