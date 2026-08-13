from enum import Enum

import allure
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class LoginTab(str, Enum):
  INTERNET_CAFE = "网吧登录"
  STAFF = "员工登录"
  AGENT = "代理商登录"


class LoginPage(BasePage):
  LOGIN_PATH = "/account/login"

  PAGE_HEADING = (By.XPATH, "//h3[contains(text(),'熊猫掌柜5.0用户登录')]")
  LOGIN_BUTTON = (By.CSS_SELECTOR, "button.btn-login")
  TEXT_BUTTONS = (By.CSS_SELECTOR, "button.el-button--text")
  FORM_ERRORS = (By.CSS_SELECTOR, ".el-form-item__error")
  MESSAGE_TOAST = (By.CSS_SELECTOR, ".el-message__content")
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
  )

  def _text_button(self, label: str, timeout: int | None = None):
    wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
    buttons = wait.until(EC.presence_of_all_elements_located(self.TEXT_BUTTONS))
    for button in buttons:
      if label in button.text:
        return button
    raise NoSuchElementException(f"未找到文本按钮: {label}")

  def _visible_message_box(self):
    for wrapper in self.driver.find_elements(By.CSS_SELECTOR, ".el-message-box__wrapper"):
      if wrapper.is_displayed():
        return wrapper
    return None

  @allure.step("打开登录页")
  def open_login(self) -> None:
    self.open(self.LOGIN_PATH)
    self.wait.until(EC.visibility_of_element_located(self.PAGE_HEADING))

  @allure.step("切换到 Tab: {tab}")
  def switch_tab(self, tab: LoginTab) -> None:
    tab_el = self.wait.until(
      EC.element_to_be_clickable((By.XPATH, f"//div[@role='tab'][normalize-space()='{tab.value}']"))
    )
    tab_el.click()
    self.wait.until(
      EC.presence_of_element_located(
        (By.XPATH, f"//div[@role='tab'][normalize-space()='{tab.value}'][@aria-selected='true']")
      )
    )

  def _input_by_placeholder(self, placeholder: str):
    return self.wait.until(
      EC.visibility_of_element_located((By.CSS_SELECTOR, f"input[placeholder='{placeholder}']"))
    )

  def _fill_by_placeholder(self, placeholder: str, value: str) -> None:
    field = self._input_by_placeholder(placeholder)
    field.click()
    field.clear()
    field.send_keys(value)

  @allure.step("填写网吧账号: {account}")
  def fill_internet_cafe_account(self, account: str) -> None:
    self._fill_by_placeholder("请输入网吧账号", account)

  @allure.step("填写员工账号: {account}")
  def fill_staff_account(self, account: str) -> None:
    self._fill_by_placeholder("请输入员工账号", account)

  @allure.step("填写代理商账号: {account}")
  def fill_agent_account(self, account: str) -> None:
    self._fill_by_placeholder("请输入代理商账号", account)

  @allure.step("填写密码")
  def fill_password(self, password: str) -> None:
    self._fill_by_placeholder("请输入密码", password)

  @allure.step("点击登录")
  def click_login(self) -> None:
    btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
    btn.click()

  def wait_for_form_errors(self, timeout: int = 5) -> list[str]:
    def _collect(_driver):
      errors = [e.text.strip() for e in _driver.find_elements(*self.FORM_ERRORS) if e.text.strip()]
      return errors if errors else None

    return WebDriverWait(self.driver, timeout).until(_collect)

  def wait_for_login_failure_feedback(self, timeout: int = 15) -> list[str]:
    error_snippets = ("该网吧账号还未注册", "密码错误", "账号或密码")

    def _collect(_driver):
      messages = [
        element.text.strip()
        for element in _driver.find_elements(*self.MESSAGE_TOAST)
        if element.is_displayed() and element.text.strip()
      ]
      if messages:
        return messages

      body_text = _driver.find_element(By.TAG_NAME, "body").text
      matched = [snippet for snippet in error_snippets if snippet in body_text]
      return matched if matched else None

    return WebDriverWait(self.driver, timeout, poll_frequency=0.2).until(_collect)

  @allure.step("网吧登录: 账号={account}")
  def login_internet_cafe(self, account: str, password: str) -> None:
    self.switch_tab(LoginTab.INTERNET_CAFE)
    self.fill_internet_cafe_account(account)
    self.fill_password(password)
    self.click_login()

  @allure.step("员工登录")
  def login_staff(self, cafe_account: str, staff_account: str, password: str) -> None:
    self.switch_tab(LoginTab.STAFF)
    self.fill_internet_cafe_account(cafe_account)
    self.fill_staff_account(staff_account)
    self.fill_password(password)
    self.click_login()

  @allure.step("代理商登录")
  def login_agent(self, account: str, password: str) -> None:
    self.switch_tab(LoginTab.AGENT)
    self.fill_agent_account(account)
    self.fill_password(password)
    self.click_login()

  @allure.step("点击忘记密码")
  def click_forgot_password(self) -> None:
    self._text_button("忘记密码").click()
    self.wait_for_url_contains("/account/password")

  @allure.step("点击注册账号")
  def click_register(self) -> None:
    self._text_button("注册账号").click()
    self.wait.until(lambda _: self._visible_message_box() is not None)

  @allure.step("关闭注册提示弹窗")
  def close_register_dialog(self) -> None:
    box = self.wait.until(lambda _: self._visible_message_box())
    confirm = box.find_element(By.CSS_SELECTOR, "button.el-button--primary")
    confirm.click()
    self.wait.until(lambda _: self._visible_message_box() is None)

  def is_forgot_password_visible(self) -> bool:
    try:
      return self._text_button("忘记密码", timeout=2).is_displayed()
    except (NoSuchElementException, TimeoutException):
      return False

  def is_register_visible(self) -> bool:
    try:
      return self._text_button("注册账号", timeout=2).is_displayed()
    except (NoSuchElementException, TimeoutException):
      return False

  def is_on_login_page(self) -> bool:
    return "/account/login" in self.current_url()

  def page_source_has_sql_error_leak(self) -> bool:
    source = self.driver.page_source.lower()
    return any(snippet in source for snippet in self.SQL_ERROR_SNIPPETS)

  @allure.step("校验恶意输入被拒绝登录")
  def assert_malicious_login_rejected(self, timeout: int = 8) -> None:
    WebDriverWait(self.driver, timeout, poll_frequency=0.2).until(
      lambda _driver: self.is_on_login_page()
    )
    assert self.is_on_login_page(), "SQL 注入 payload 不应导致登录成功跳转"
    assert not self.page_source_has_sql_error_leak(), "页面不应泄露数据库/SQL 错误信息"

  def is_placeholder_visible(self, placeholder: str) -> bool:
    locator = (By.CSS_SELECTOR, f"input[placeholder='{placeholder}']")
    try:
      WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(locator))
      return True
    except TimeoutException:
      return False

  def is_register_dialog_visible(self) -> bool:
    return self._visible_message_box() is not None

  def get_register_dialog_text(self) -> str:
    box = self.wait.until(lambda _: self._visible_message_box())
    message = box.find_element(By.CSS_SELECTOR, ".el-message-box__message")
    return message.text
