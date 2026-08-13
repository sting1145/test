import allure
import pytest

from pages.login_page import LoginTab
from utils.allure_decorators import testcase
from utils.config import Config
from utils.sql_injection_payloads import (
  ACCOUNT_PAYLOADS,
  ALL_ACCOUNT_PAYLOADS,
  PASSWORD_PAYLOADS,
)

pytestmark = [pytest.mark.ui, pytest.mark.login]


@allure.epic("熊猫掌柜")
@allure.feature("登录模块")
@pytest.mark.smoke
class TestLoginPageLoad:
  @testcase("TC-LOGIN-001")
  def test_login_page_loads_with_core_elements(self, login_page):
    login_page.open_login()
    assert "熊猫掌柜用户管理系统" in login_page.page_title()
    assert login_page.is_on_login_page()
    assert login_page.is_placeholder_visible("请输入网吧账号")
    assert login_page.is_placeholder_visible("请输入密码")

  @testcase("TC-LOGIN-002")
  def test_auxiliary_links_visible(self, login_page):
    login_page.open_login()
    assert login_page.is_forgot_password_visible()
    assert login_page.is_register_visible()


@allure.story("网吧登录-表单校验")
@pytest.mark.negative
class TestInternetCafeValidation:
  @pytest.fixture(autouse=True)
  def setup(self, login_page):
    login_page.open_login()
    login_page.switch_tab(LoginTab.INTERNET_CAFE)

  @testcase("TC-LOGIN-003")
  def test_empty_form_shows_required_errors(self, login_page):
    login_page.click_login()
    errors = login_page.wait_for_form_errors()
    assert "请输入网吧账号" in errors
    assert "请输入密码" in errors
    assert login_page.is_on_login_page()

  @testcase("TC-LOGIN-004")
  def test_missing_password_shows_error(self, login_page):
    login_page.fill_internet_cafe_account("test_account")
    login_page.click_login()
    errors = login_page.wait_for_form_errors()
    assert "请输入密码" in errors
    assert login_page.is_on_login_page()

  @testcase("TC-LOGIN-005")
  def test_missing_account_shows_error(self, login_page):
    login_page.fill_password("test_password")
    login_page.click_login()
    errors = login_page.wait_for_form_errors()
    assert "请输入网吧账号" in errors
    assert login_page.is_on_login_page()


@allure.story("员工登录-表单校验")
@pytest.mark.negative
class TestStaffValidation:
  @pytest.fixture(autouse=True)
  def setup(self, login_page):
    login_page.open_login()
    login_page.switch_tab(LoginTab.STAFF)

  @testcase("TC-LOGIN-006")
  def test_staff_tab_shows_three_fields(self, login_page):
    assert login_page.is_placeholder_visible("请输入网吧账号")
    assert login_page.is_placeholder_visible("请输入员工账号")
    assert login_page.is_placeholder_visible("请输入密码")

  @testcase("TC-LOGIN-007")
  def test_empty_form_shows_all_required_errors(self, login_page):
    login_page.click_login()
    errors = login_page.wait_for_form_errors()
    assert "请输入网吧账号" in errors
    assert "请输入员工账号" in errors
    assert "请输入密码" in errors
    assert login_page.is_on_login_page()


@allure.story("代理商登录-表单校验")
@pytest.mark.negative
class TestAgentValidation:
  @pytest.fixture(autouse=True)
  def setup(self, login_page):
    login_page.open_login()
    login_page.switch_tab(LoginTab.AGENT)

  @testcase("TC-LOGIN-008")
  def test_agent_tab_shows_fields(self, login_page):
    assert login_page.is_placeholder_visible("请输入代理商账号")
    assert login_page.is_placeholder_visible("请输入密码")

  @testcase("TC-LOGIN-009")
  def test_empty_form_shows_required_errors(self, login_page):
    login_page.click_login()
    errors = login_page.wait_for_form_errors()
    assert "请输入代理商账号" in errors
    assert "请输入密码" in errors
    assert login_page.is_on_login_page()


@allure.story("Tab切换")
class TestTabSwitching:
  @testcase("TC-LOGIN-010")
  def test_tabs_switch_form_fields(self, login_page):
    login_page.open_login()

    assert login_page.is_placeholder_visible("请输入网吧账号")

    login_page.switch_tab(LoginTab.STAFF)
    assert login_page.is_placeholder_visible("请输入员工账号")

    login_page.switch_tab(LoginTab.AGENT)
    assert login_page.is_placeholder_visible("请输入代理商账号")

    login_page.switch_tab(LoginTab.INTERNET_CAFE)
    assert login_page.is_placeholder_visible("请输入网吧账号")


@allure.story("错误凭证")
@pytest.mark.negative
class TestInvalidCredentials:
  @testcase("TC-LOGIN-011")
  def test_wrong_credentials_stays_on_login_page(self, login_page):
    login_page.open_login()
    login_page.login_internet_cafe("invalid_test_account_12345", "wrong_password_123")
    assert login_page.is_on_login_page()
    messages = login_page.wait_for_login_failure_feedback()
    assert any("该网吧账号还未注册" in message for message in messages)


@allure.story("SQL注入防护")
@pytest.mark.negative
@pytest.mark.security
class TestSqlInjection:
  SAFE_PASSWORD = "test_password_123"
  SAFE_ACCOUNT = "test_account_123"

  @pytest.fixture(autouse=True)
  def setup(self, login_page):
    login_page.open_login()
    login_page.switch_tab(LoginTab.INTERNET_CAFE)

  @testcase("TC-LOGIN-014")
  @pytest.mark.parametrize("payload", ALL_ACCOUNT_PAYLOADS, ids=lambda value: value[:40])
  def test_sql_injection_in_account_field_rejected(self, login_page, payload):
    login_page.fill_internet_cafe_account(payload)
    login_page.fill_password(self.SAFE_PASSWORD)
    login_page.click_login()
    login_page.assert_malicious_login_rejected()

  @testcase("TC-LOGIN-015")
  @pytest.mark.parametrize("payload", PASSWORD_PAYLOADS, ids=lambda value: value[:40])
  def test_sql_injection_in_password_field_rejected(self, login_page, payload):
    login_page.fill_internet_cafe_account(self.SAFE_ACCOUNT)
    login_page.fill_password(payload)
    login_page.click_login()
    login_page.assert_malicious_login_rejected()

  @testcase("TC-LOGIN-016")
  @pytest.mark.parametrize("payload", ACCOUNT_PAYLOADS, ids=lambda value: value[:40])
  def test_sql_injection_in_both_fields_rejected(self, login_page, payload):
    login_page.fill_internet_cafe_account(payload)
    login_page.fill_password(payload)
    login_page.click_login()
    login_page.assert_malicious_login_rejected()


@allure.story("辅助入口")
class TestAuxiliaryActions:
  @testcase("TC-LOGIN-012")
  def test_forgot_password_navigates_to_reset_page(self, login_page, password_reset_page):
    login_page.open_login()
    login_page.click_forgot_password()
    assert password_reset_page.is_loaded()
    assert password_reset_page.has_mobile_recovery()
    assert password_reset_page.has_email_recovery()
    assert password_reset_page.has_next_step_button()
    assert password_reset_page.has_back_to_login_link()

  @testcase("TC-LOGIN-013")
  def test_register_shows_stop_registration_dialog(self, login_page):
    login_page.open_login()
    login_page.click_register()
    assert login_page.is_register_dialog_visible()
    text = login_page.get_register_dialog_text()
    assert "现已停止网吧自主注册" in text
    assert "区域经理" in text
    login_page.close_register_dialog()
    assert login_page.is_on_login_page()


@pytest.mark.positive
class TestSuccessfulLogin:
  @testcase("TC-LOGIN-017")
  def test_internet_cafe_login_success(self, login_page):
    if not Config.INTERNET_CAFE_ACCOUNT or not Config.INTERNET_CAFE_PASSWORD:
      pytest.skip("请在 .env 中配置 INTERNET_CAFE_ACCOUNT 和 INTERNET_CAFE_PASSWORD")

    login_page.open_login()
    login_page.login_internet_cafe(Config.INTERNET_CAFE_ACCOUNT, Config.INTERNET_CAFE_PASSWORD)
    assert not login_page.is_on_login_page()

  @testcase("TC-LOGIN-018")
  def test_staff_login_success(self, login_page):
    if not Config.STAFF_CAFE_ACCOUNT or not Config.STAFF_ACCOUNT or not Config.STAFF_PASSWORD:
      pytest.skip("请在 .env 中配置员工登录测试账号")

    login_page.open_login()
    login_page.login_staff(
      Config.STAFF_CAFE_ACCOUNT,
      Config.STAFF_ACCOUNT,
      Config.STAFF_PASSWORD,
    )
    assert not login_page.is_on_login_page()

  @testcase("TC-LOGIN-019")
  def test_agent_login_success(self, login_page):
    if not Config.AGENT_ACCOUNT or not Config.AGENT_PASSWORD:
      pytest.skip("请在 .env 中配置 AGENT_ACCOUNT 和 AGENT_PASSWORD")

    login_page.open_login()
    login_page.login_agent(Config.AGENT_ACCOUNT, Config.AGENT_PASSWORD)
    assert not login_page.is_on_login_page()


@allure.story("报告截图演示")
class TestScreenshotDemo:
  """故意失败的用例，用于预览 Allure 报告中的失败截图。看完效果后可删除此类。"""

  @allure.title("【演示】故意失败以预览报告截图")
  @allure.severity(allure.severity_level.MINOR)
  def test_intentional_failure_for_screenshot_demo(self, login_page):
    login_page.open_login()
    assert "这个标题不存在" in login_page.page_title()
