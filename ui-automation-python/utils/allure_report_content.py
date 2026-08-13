"""构建 Allure 报告中的前置条件、测试数据等描述内容。"""

from collections.abc import Callable
from typing import Any

from utils.config import Config

_EMPTY_DATA = {"无", "none", "n/a", ""}


def mask_secret(value: str, *, visible_start: int = 10, visible_end: int = 4) -> str:
  text = str(value).strip()
  if not text:
    return "(空)"
  if len(text) <= visible_start + visible_end:
    return "***"
  return f"{text[:visible_start]}...{text[-visible_end:]}"


def _normalize_data_block(data: str | None) -> str | None:
  if data is None:
    return None
  text = str(data).strip()
  if not text or text.lower() in _EMPTY_DATA:
    return None
  return text


def build_allure_description(
  case: dict,
  *,
  runtime_data: str | None = None,
) -> str:
  sections: list[str] = [f"前置条件：\n{case['precondition']}"]

  data_parts: list[str] = []
  runtime_block = _normalize_data_block(runtime_data)
  if runtime_block:
    data_parts.append(runtime_block)
  else:
    static_data = _normalize_data_block(case.get("data"))
    if static_data:
      data_parts.append(static_data)

  if data_parts:
    sections.append("测试数据：\n" + "\n\n".join(data_parts))

  sections.append(f"测试步骤：\n{case['steps']}")
  sections.append(f"预期结果：\n{case['expected']}")
  return "\n\n".join(sections)


def format_key_values(pairs: list[tuple[str, Any]], *, mask_keys: set[str] | None = None) -> str:
  mask_keys = mask_keys or set()
  lines: list[str] = []
  for key, value in pairs:
    text = str(value).strip() if value is not None else ""
    if not text:
      display = "(未配置)"
    elif any(token in key.lower() for token in mask_keys):
      display = mask_secret(text)
    else:
      display = text
    lines.append(f"{key}：{display}")
  return "\n".join(lines)


def format_sql_injection_runtime_data(
  *,
  payload: str,
  field: str,
  safe_user: str = "",
  safe_password: str = "",
  hash_password: bool | None = None,
) -> str:
  lines = [f"注入字段：{field}", f"payload：{payload}"]
  if safe_user:
    lines.append(f"对照账号(user_name)：{safe_user}")
  if safe_password:
    lines.append(f"对照密码(password)：{mask_secret(safe_password)}")
  if hash_password is True:
    lines.append("password 提交方式：MD5 后提交")
  elif hash_password is False:
    lines.append("password 提交方式：明文提交")
  lines.append("captcha：(空)")
  return "\n".join(lines)


def format_session_probe_runtime_data(path: str) -> str:
  return format_key_values(
    [
      ("受保护接口", f"{Config.API_BASE_URL}{path}"),
      ("请求方式", "GET（无 Cookie）"),
    ]
  )


def format_session_auth_runtime_data() -> str:
  return format_key_values(
    [
      ("SESSION_ACCOUNT_B", Config.SESSION_ACCOUNT_B or "(未配置)"),
      ("API_CURRENT_USER_PATH", Config.API_CURRENT_USER_PATH),
      ("API_LIST_PATH", Config.API_LIST_PATH),
      ("API_USER_REFERER", Config.API_USER_REFERER),
      ("API_LIST_REFERER", Config.API_LIST_REFERER),
      ("SESSION_COOKIE_B", Config.SESSION_COOKIE_B),
    ],
    mask_keys={"cookie", "password"},
  )


def format_positive_login_runtime_data(login_type: str) -> str:
  if login_type == "internet_cafe":
    pairs = [
      ("登录类型", "网吧登录"),
      ("网吧账号", Config.INTERNET_CAFE_ACCOUNT),
      ("密码", Config.INTERNET_CAFE_PASSWORD),
    ]
  elif login_type == "staff":
    pairs = [
      ("登录类型", "员工登录"),
      ("网吧账号", Config.STAFF_CAFE_ACCOUNT),
      ("员工账号", Config.STAFF_ACCOUNT),
      ("密码", Config.STAFF_PASSWORD),
    ]
  else:
    pairs = [
      ("登录类型", "代理商登录"),
      ("代理商账号", Config.AGENT_ACCOUNT),
      ("密码", Config.AGENT_PASSWORD),
    ]
  return format_key_values(pairs, mask_keys={"password"})


API_RUNTIME_DATA_RESOLVERS: dict[str, Callable[..., str | None]] = {
  "TC-SESSION-007": lambda **kwargs: format_session_probe_runtime_data(
    kwargs.get("path") or Config.API_CURRENT_USER_PATH.strip() or Config.API_LIST_PATH.strip()
  ),
  "TC-SESSION-014": lambda **_kwargs: format_session_auth_runtime_data(),
}

API_METHOD_RUNTIME_BUILDERS: dict[str, Callable[..., str | None]] = {
  "test_sql_injection_in_user_name_rejected": lambda **kwargs: format_sql_injection_runtime_data(
    payload=kwargs["payload"],
    field="user_name",
    safe_password=kwargs.get("safe_password", ""),
  ),
  "test_sql_injection_in_password_plain_rejected": lambda **kwargs: format_sql_injection_runtime_data(
    payload=kwargs["payload"],
    field="password",
    safe_user=kwargs.get("safe_user", ""),
    hash_password=False,
  ),
  "test_sql_injection_in_password_hashed_rejected": lambda **kwargs: format_sql_injection_runtime_data(
    payload=kwargs["payload"],
    field="password",
    safe_user=kwargs.get("safe_user", ""),
    hash_password=True,
  ),
  "test_sql_injection_in_both_fields_rejected": lambda **kwargs: format_sql_injection_runtime_data(
    payload=kwargs["payload"],
    field="user_name + password",
    hash_password=False,
  ),
}

UI_METHOD_RUNTIME_BUILDERS: dict[str, Callable[..., str | None]] = {
  "test_sql_injection_in_account_field_rejected": lambda **kwargs: format_sql_injection_runtime_data(
    payload=kwargs["payload"],
    field="网吧账号",
    safe_password=kwargs.get("safe_password", ""),
  ),
  "test_sql_injection_in_password_field_rejected": lambda **kwargs: format_sql_injection_runtime_data(
    payload=kwargs["payload"],
    field="密码",
    safe_user=kwargs.get("safe_account", ""),
  ),
  "test_sql_injection_in_both_fields_rejected": lambda **kwargs: format_sql_injection_runtime_data(
    payload=kwargs["payload"],
    field="网吧账号 + 密码",
  ),
  "test_wrong_credentials_stays_on_login_page": lambda **_kwargs: (
    "账号：invalid_test_account_12345\n密码：wrong_password_123"
  ),
  "test_internet_cafe_login_success": lambda **_kwargs: format_positive_login_runtime_data("internet_cafe"),
  "test_staff_login_success": lambda **_kwargs: format_positive_login_runtime_data("staff"),
  "test_agent_login_success": lambda **_kwargs: format_positive_login_runtime_data("agent"),
}


def resolve_runtime_data(
  *,
  case_id: str,
  method_name: str,
  bound_args: dict[str, Any],
  resolvers: dict[str, Callable[..., str | None]],
  method_builders: dict[str, Callable[..., str | None]],
) -> str | None:
  if case_id in resolvers:
    return resolvers[case_id](**bound_args)

  builder = method_builders.get(method_name)
  if not builder:
    return None

  try:
    return builder(**bound_args)
  except (KeyError, TypeError):
    return None


def inject_bound_test_constants(bound_args: dict[str, Any], test_instance: Any | None) -> dict[str, Any]:
  enriched = dict(bound_args)
  if test_instance is None:
    return enriched

  for attr, key in (
    ("SAFE_PASSWORD", "safe_password"),
    ("SAFE_ACCOUNT", "safe_account"),
    ("SAFE_USER", "safe_user"),
  ):
    if key not in enriched and hasattr(test_instance, attr):
      enriched[key] = getattr(test_instance, attr)
  return enriched
