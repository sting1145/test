import json

from api.clients.passport_client import ApiResponse

SQL_ERROR_SNIPPETS = (
  "sql syntax",
  "mysql",
  "sqlite",
  "ora-",
  "postgresql",
  "sqlserver",
  "syntax error",
  "unclosed quotation",
  "quoted string not properly terminated",
  "odbc",
)


def response_text_has_sql_leak(response: ApiResponse) -> bool:
  body = response.text.lower()
  return any(snippet in body for snippet in SQL_ERROR_SNIPPETS)


def _parse_json(response: ApiResponse) -> dict | None:
  try:
    return json.loads(response.text)
  except json.JSONDecodeError:
    return None


def is_login_success(response: ApiResponse) -> bool:
  if response.status_code >= 500:
    return False

  data = _parse_json(response)
  if not isinstance(data, dict):
    return False

  if data.get("token") or data.get("access_token"):
    return True

  nested = data.get("data")
  if isinstance(nested, dict) and (nested.get("token") or nested.get("access_token")):
    return True

  code = data.get("code")
  if code in (0, "0", 200, "200"):
    return True

  if data.get("success") is True:
    return True

  return False


def assert_sql_injection_blocked(response: ApiResponse, *, context: str = "") -> None:
  prefix = f"{context}: " if context else ""

  assert not is_login_success(response), (
    f"{prefix}SQL 注入 payload 不应导致登录成功，status={response.status_code}, body={response.text[:300]}"
  )
  assert not response_text_has_sql_leak(response), (
    f"{prefix}响应中泄露数据库/SQL 错误信息: {response.text[:300]}"
  )
  assert response.status_code < 500, (
    f"{prefix}服务端不应返回 5xx，status={response.status_code}, body={response.text[:300]}"
  )
