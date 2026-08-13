from playwright.sync_api import Page, expect


class BasePage:
  def __init__(self, page: Page, base_url: str):
    self.page = page
    self.base_url = base_url.rstrip("/")

  def open(self, path: str = "/") -> None:
    self.page.goto(f"{self.base_url}{path}")

  def expect_url_contains(self, fragment: str) -> None:
    expect(self.page).to_have_url(fragment)
