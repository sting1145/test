import allure
import pytest

from utils.api_allure_decorators import api_testcase
from utils.api_request_headers import api_referer_for
from utils.api_session_assertions import (
  assert_api_success,
  assert_unauthenticated,
  assert_user_identity_consistent,
)
from utils.config import Config


def _require_both_api_paths() -> tuple[str, str]:
  current_user = Config.API_CURRENT_USER_PATH.strip()
  list_path = Config.API_LIST_PATH.strip()
  if not current_user or not list_path:
    pytest.skip("未配置 API_CURRENT_USER_PATH 和 API_LIST_PATH，请从 Network 复制接口路径")
  return current_user, list_path


def _get_with_referer(client, path: str):
  return client.get(path, headers={"Referer": api_referer_for(path)})


@allure.epic("熊猫掌柜")
@allure.feature("会话与状态")
@pytest.mark.api
@pytest.mark.session
class TestSessionApi:
  @api_testcase("TC-SESSION-007")
  def test_protected_api_rejects_without_session(self, anonymous_client):
    path = Config.API_CURRENT_USER_PATH.strip() or Config.API_LIST_PATH.strip()
    if not path:
      pytest.skip("未配置 API_CURRENT_USER_PATH 或 API_LIST_PATH")

    response = _get_with_referer(anonymous_client, path)
    assert_unauthenticated(response, context=path)

  @api_testcase("TC-SESSION-014")
  def test_current_user_matches_list_api(self, authenticated_client):
    current_user_path, list_path = _require_both_api_paths()

    current_user_response = _get_with_referer(authenticated_client, current_user_path)
    current_user_payload = assert_api_success(
      current_user_response,
      context=current_user_path,
    )

    list_response = _get_with_referer(authenticated_client, list_path)
    list_payload = assert_api_success(list_response, context=list_path)

    assert_user_identity_consistent(
      current_user_payload,
      list_payload,
      expected_account=Config.SESSION_ACCOUNT_B,
      context="current-user vs list",
    )
