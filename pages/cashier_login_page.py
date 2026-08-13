import re

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from utils.cashier_auth import (
  attempt_cashier_login,
  perform_cashier_login,
  read_stored_user_info,
)


class CashierLoginPage(BasePage):
  LOGIN_PATH = "/html/login.html#/"

  def __init__(self, page: Page, base_url: str):
    super().__init__(page, base_url)

  @property
  def slogan(self):
    return self.page.get_by_text("熊猫掌柜，网吧营销专家")

  @property
  def login_button(self):
    return self.page.locator(".login-btn")

  @property
  def error_text(self):
    return self.page.locator(".error.fs13")

  @property
  def account_input(self):
    return self.page.locator("#account-id")

  @property
  def password_input(self):
    return self.page.locator('input[type="password"]')

  def ip_input(self, index: int):
    return self.page.locator(f"#ipInput{index}")

  def open_login(self) -> None:
    self.open(self.LOGIN_PATH)
    expect(self.slogan).to_be_visible()

  def fill_server_ip(self, ip: str) -> None:
    segments = ip.split(".")
    if len(segments) != 4:
      raise ValueError(f"服务器 IP 格式不正确：{ip}")

    for index, segment in enumerate(segments):
      self.ip_input(index).fill(segment)

  def fill_account(self, account: str) -> None:
    self.account_input.fill(account)

  def fill_password(self, password: str) -> None:
    self.password_input.fill(password)

  def click_login(self) -> None:
    self.login_button.click()

  def login(self, server_ip: str, account: str, password: str) -> None:
    self.fill_server_ip(server_ip)
    self.fill_account(account)
    self.fill_password(password)
    perform_cashier_login(
      self.page,
      server_ip=server_ip,
      account=account,
      password=password,
      click_login=self.click_login,
    )

  def login_attempt(self, server_ip: str, account: str, password: str) -> dict:
    self.fill_server_ip(server_ip)
    self.fill_account(account)
    self.fill_password(password)
    return attempt_cashier_login(
      self.page,
      server_ip=server_ip,
      account=account,
      password=password,
      click_login=self.click_login,
    )

  def expect_page_loaded(self) -> None:
    expect(self.page).to_have_url(re.compile(r"/html/login\.html"))
    expect(self.slogan).to_be_visible()
    expect(self.page.get_by_text("服务器IP", exact=True)).to_be_visible()
    expect(self.page.get_by_text("账号", exact=True)).to_be_visible()
    expect(self.page.get_by_text("密码", exact=True)).to_be_visible()
    expect(self.login_button).to_be_visible()
    expect(self.page.get_by_text("记住密码", exact=True)).to_be_visible()
    expect(self.page.get_by_text("忘记密码", exact=True)).to_be_visible()
    expect(self.page.get_by_text("扫码登录", exact=True)).to_be_visible()
    expect(self.account_input).to_be_visible()
    expect(self.password_input).to_be_visible()

  def expect_ip_fields_visible(self) -> None:
    for index in range(4):
      expect(self.ip_input(index)).to_be_visible()

  def expect_validation_error(self, message: str) -> None:
    expect(self.error_text).to_contain_text(message)

  def expect_stay_on_login_page(self) -> None:
    expect(self.page).to_have_url(re.compile(r"/html/login\.html"))

  def expect_login_success(self, timeout: int = 15_000) -> None:
    deadline_ms = self.page.evaluate("() => Date.now()") + timeout

    while True:
      user_info = read_stored_user_info(self.page)
      if user_info and user_info.get("auth"):
        return

      error_message = self.error_text.inner_text().strip()
      if error_message:
        raise AssertionError(f"登录失败，页面提示：{error_message}")

      if self.page.evaluate("() => Date.now()") >= deadline_ms:
        raise AssertionError("登录超时：未写入 userinfo，且页面无明确错误提示")

      self.page.wait_for_timeout(200)

  def expect_login_failure(self, message: str | None = None) -> None:
    self.page.wait_for_timeout(1000)
    user_info = read_stored_user_info(self.page)
    assert user_info is None

    if message:
      expect(self.error_text).to_contain_text(message, timeout=10_000)
    else:
      expect(self.error_text).not_to_be_empty()
