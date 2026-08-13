import allure
import pytest

from utils.allure_decorators import apply_chinese_title
from utils.config import Config

pytestmark = [pytest.mark.ui, pytest.mark.login]


@allure.epic("熊猫掌柜收银台")
@allure.feature("登录模块")
class TestCashierLoginPageLoad:
  @apply_chinese_title
  @allure.story("页面加载")
  @allure.severity(allure.severity_level.CRITICAL)
  def test_should_load_login_page_with_core_elements(self, cashier_login_page):
    cashier_login_page.open_login()
    cashier_login_page.expect_page_loaded()
    cashier_login_page.expect_ip_fields_visible()


@allure.epic("熊猫掌柜收银台")
@allure.feature("登录模块")
@allure.story("表单校验")
class TestCashierLoginValidation:
  @pytest.fixture(autouse=True)
  def _open_login(self, cashier_login_page):
    cashier_login_page.open_login()

  @apply_chinese_title
  @pytest.mark.negative
  @allure.severity(allure.severity_level.NORMAL)
  def test_should_require_server_ip_account_and_password(self, cashier_login_page):
    cashier_login_page.click_login()
    cashier_login_page.expect_validation_error("请输入服务器IP")
    cashier_login_page.expect_stay_on_login_page()

  @apply_chinese_title
  @pytest.mark.negative
  @allure.severity(allure.severity_level.NORMAL)
  def test_should_require_account_when_only_ip_filled(self, cashier_login_page):
    cashier_login_page.fill_server_ip(Config.CASHIER_SERVER_IP)
    cashier_login_page.click_login()
    cashier_login_page.expect_validation_error("请输入账号")
    cashier_login_page.expect_stay_on_login_page()

  @apply_chinese_title
  @pytest.mark.negative
  @allure.severity(allure.severity_level.NORMAL)
  def test_should_require_password_when_ip_and_account_filled(self, cashier_login_page):
    cashier_login_page.fill_server_ip(Config.CASHIER_SERVER_IP)
    cashier_login_page.fill_account(Config.CASHIER_ACCOUNT)
    cashier_login_page.click_login()
    cashier_login_page.expect_validation_error("请输入密码")
    cashier_login_page.expect_stay_on_login_page()


@allure.epic("熊猫掌柜收银台")
@allure.feature("登录模块")
@allure.story("正向登录")
class TestCashierPositiveLogin:
  @apply_chinese_title
  @pytest.mark.positive
  @pytest.mark.smoke
  @allure.severity(allure.severity_level.CRITICAL)
  def test_should_login_successfully_with_valid_credentials(self, cashier_login_page):
    cashier_login_page.open_login()
    cashier_login_page.login(
      Config.CASHIER_SERVER_IP,
      Config.CASHIER_ACCOUNT,
      Config.CASHIER_PASSWORD,
    )
    cashier_login_page.expect_login_success()


@allure.epic("熊猫掌柜收银台")
@allure.feature("登录模块")
@allure.story("正向登录")
class TestCashierPassword1234567Login:
  @apply_chinese_title
  @pytest.mark.positive
  @allure.severity(allure.severity_level.NORMAL)
  def test_should_login_successfully_when_password_is_1234567(self, cashier_login_page):
    cashier_login_page.open_login()
    cashier_login_page.login_attempt(
      Config.CASHIER_SERVER_IP,
      Config.CASHIER_ACCOUNT,
      "1234567",
    )
    cashier_login_page.expect_login_success()
