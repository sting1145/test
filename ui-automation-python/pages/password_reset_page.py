from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class PasswordResetPage(BasePage):
  RESET_PATH_FRAGMENT = "/account/password"
  MOBILE_RECOVERY = (By.XPATH, "//*[contains(normalize-space(),'手机找回密码')]")
  EMAIL_RECOVERY = (By.XPATH, "//*[contains(normalize-space(),'使用邮箱找回密码')]")
  NEXT_STEP_BUTTON = (By.XPATH, "//button[contains(normalize-space(),'下一步')]")
  BACK_TO_LOGIN = (By.XPATH, "//*[contains(normalize-space(),'已有账号，立即登录')]")

  def is_loaded(self) -> bool:
    return self.RESET_PATH_FRAGMENT in self.current_url()

  def _has_visible(self, locator: tuple[str, str]) -> bool:
    return any(element.is_displayed() for element in self.driver.find_elements(*locator))

  def has_mobile_recovery(self) -> bool:
    return self._has_visible(self.MOBILE_RECOVERY)

  def has_email_recovery(self) -> bool:
    return self._has_visible(self.EMAIL_RECOVERY)

  def has_next_step_button(self) -> bool:
    return self._has_visible(self.NEXT_STEP_BUTTON)

  def has_back_to_login_link(self) -> bool:
    return self._has_visible(self.BACK_TO_LOGIN)
