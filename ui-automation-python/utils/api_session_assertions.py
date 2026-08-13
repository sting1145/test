import json
from typing import Any

from api.clients.passport_client import ApiResponse


def _parse_json(response: ApiResponse) -> dict | list | None:
  try:
    return json.loads(response.text)
  except json.JSONDecodeError:
    return None


def _walk_values(node: Any):
  if isinstance(node, dict):
    for value in node.values():
      yield from _walk_values(value)
  elif isinstance(node, list):
    for item in node:
      yield from _walk_values(item)
  elif node is not None:
    yield node


def extract_user_identifiers(payload: dict | list | None) -> set[str]:
  if payload is None:
    return set()

  keys = {
    "userid",
    "user_id",
    "account",
    "username",
    "user_name",
    "loginname",
    "login_name",
    "login_id",
    "nid",
    "mobile",
    "phone",
    "name",
    "nickname",
    "nick_name",
  }
  identifiers: set[str] = set()

  def walk(node: Any, parent_key: str = "") -> None:
    if isinstance(node, dict):
      for key, value in node.items():
        normalized = str(key).lower()
        if normalized in keys and value not in (None, ""):
          identifiers.add(str(value).strip().lower())
        walk(value, normalized)
    elif isinstance(node, list):
      for item in node:
        walk(item, parent_key)

  walk(payload)
  return identifiers


def assert_api_success(response: ApiResponse, *, context: str = "") -> dict | list:
  prefix = f"{context}: " if context else ""
  assert response.status_code < 500, (
    f"{prefix}接口不应返回 5xx，status={response.status_code}, body={response.text[:300]}"
  )

  payload = _parse_json(response)
  if isinstance(payload, dict):
    biz_status = payload.get("status")
    code = payload.get("code")
    if biz_status in (40005, "40005", 401, "401", 403, "403"):
      raise AssertionError(
        f"{prefix}接口要求登录或会话已失效，body={response.text[:300]}"
      )
    if biz_status not in (None, 200, "200", 0, "0") and code in (404, "404"):
      raise AssertionError(
        f"{prefix}接口返回业务 404，status={response.status_code}, body={response.text[:300]}"
      )
    if biz_status not in (None, 200, "200", 0, "0") and code not in (None, 0, "0", 200, "200"):
      if payload.get("success") is not True:
        raise AssertionError(
          f"{prefix}接口业务失败，status={response.status_code}, body={response.text[:300]}"
        )

  assert payload is not None, (
    f"{prefix}响应不是合法 JSON，status={response.status_code}, body={response.text[:300]}"
  )
  return payload


def assert_unauthenticated(response: ApiResponse, *, context: str = "") -> None:
  prefix = f"{context}: " if context else ""
  if response.status_code in (401, 403):
    return

  payload = _parse_json(response)
  if isinstance(payload, dict):
    code = payload.get("code")
    status = payload.get("status")
    if code in (401, 403, 10001, 10002, "401", "403") or status in (
      401,
      403,
      40005,
      "401",
      "403",
      "40005",
    ):
      return

  raise AssertionError(
    f"{prefix}未登录访问应被拒绝，status={response.status_code}, body={response.text[:300]}"
  )


def assert_user_identity_consistent(
  current_user_payload: dict | list,
  list_payload: dict | list,
  *,
  expected_account: str = "",
  context: str = "",
) -> None:
  prefix = f"{context}: " if context else ""
  current_ids = extract_user_identifiers(current_user_payload)
  list_ids = extract_user_identifiers(list_payload)

  if expected_account:
    expected = expected_account.strip().lower()
    assert expected in current_ids or any(expected in value for value in current_ids), (
      f"{prefix}current-user 未包含账号 {expected_account}，identifiers={sorted(current_ids)}"
    )

  overlap = current_ids & list_ids
  assert overlap, (
    f"{prefix}current-user 与列表接口账号标识不一致\n"
    f"current-user: {sorted(current_ids)}\n"
    f"list: {sorted(list_ids)}"
  )
