import allure
import pytest

from utils.api_allure_decorators import api_testcase
from utils.api_assertions import assert_sql_injection_blocked
from utils.sql_injection_payloads import (
  ACCOUNT_PAYLOADS,
  ALL_ACCOUNT_PAYLOADS,
  PASSWORD_PAYLOADS,
)

SAFE_USER = "test_account_api_001"
SAFE_PASSWORD = "test_password_123"


@allure.epic("熊猫掌柜")
@allure.feature("登录接口")
@allure.story("SQL注入防护")
@pytest.mark.api
@pytest.mark.security
class TestLoginApiSqlInjection:
  SAFE_USER = SAFE_USER
  SAFE_PASSWORD = SAFE_PASSWORD

  @api_testcase("TC-API-LOGIN-001")
  @pytest.mark.parametrize("payload", ALL_ACCOUNT_PAYLOADS, ids=lambda value: value[:40])
  def test_sql_injection_in_user_name_rejected(self, passport_client, payload):
    response = passport_client.login(payload, SAFE_PASSWORD, captcha="")
    passport_client._last_response = response
    assert_sql_injection_blocked(response, context=f"user_name={payload[:30]}")

  @api_testcase("TC-API-LOGIN-002")
  @pytest.mark.parametrize("payload", PASSWORD_PAYLOADS, ids=lambda value: value[:40])
  def test_sql_injection_in_password_plain_rejected(self, passport_client, payload):
    response = passport_client.login(
      SAFE_USER,
      payload,
      captcha="",
      hash_password=False,
    )
    passport_client._last_response = response
    assert_sql_injection_blocked(response, context=f"password_plain={payload[:30]}")

  @api_testcase("TC-API-LOGIN-003")
  @pytest.mark.parametrize("payload", PASSWORD_PAYLOADS, ids=lambda value: value[:40])
  def test_sql_injection_in_password_hashed_rejected(self, passport_client, payload):
    response = passport_client.login(SAFE_USER, payload, captcha="")
    passport_client._last_response = response
    assert_sql_injection_blocked(response, context=f"password_md5={payload[:30]}")

  @api_testcase("TC-API-LOGIN-004")
  @pytest.mark.parametrize("payload", ACCOUNT_PAYLOADS, ids=lambda value: value[:40])
  def test_sql_injection_in_both_fields_rejected(self, passport_client, payload):
    response = passport_client.login(
      payload,
      payload,
      captcha="",
      hash_password=False,
    )
    passport_client._last_response = response
    assert_sql_injection_blocked(response, context=f"both={payload[:30]}")
