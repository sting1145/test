from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
  def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10):
    self.driver = driver
    self.base_url = base_url.rstrip("/")
    self.wait = WebDriverWait(driver, timeout)

  def open(self, path: str = "/") -> None:
    url = f"{self.base_url}{path}"
    self.driver.get(url)

  def wait_for_url_contains(self, fragment: str) -> None:
    self.wait.until(lambda d: fragment in d.current_url)

  def current_url(self) -> str:
    return self.driver.current_url

  def page_title(self) -> str:
    return self.driver.title
