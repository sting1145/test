import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


class Config:
  BASE_URL = os.getenv("BASE_URL", "https://passport.xiongmaozhanggui.com")
  API_BASE_URL = os.getenv("API_BASE_URL", BASE_URL)
  HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
  EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", os.getenv("IMPLICIT_WAIT", "10")))
  PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
  API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
  SCREENSHOT_DIR = ROOT_DIR / "screenshots"

  SESSION_ACCOUNT_B = os.getenv("SESSION_ACCOUNT_B", "")
  SESSION_COOKIE_B = os.getenv("SESSION_COOKIE_B", "")
  SESSION_ACCOUNT_A = os.getenv("SESSION_ACCOUNT_A", "")
  SESSION_COOKIE_A = os.getenv("SESSION_COOKIE_A", "")

  API_CURRENT_USER_PATH = os.getenv("API_CURRENT_USER_PATH", "")
  API_LIST_PATH = os.getenv("API_LIST_PATH", "")
  API_LOGOUT_PATH = os.getenv("API_LOGOUT_PATH", "/api/v1/logout")
  _default_base = os.getenv("BASE_URL", "https://passport.xiongmaozhanggui.com")
  API_LIST_REFERER = os.getenv(
    "API_LIST_REFERER",
    f"{_default_base}/goods/goods_list",
  )
  API_USER_REFERER = os.getenv("API_USER_REFERER", f"{_default_base}/home")
  API_REFERER = os.getenv("API_REFERER", API_LIST_REFERER)

  INTERNET_CAFE_ACCOUNT = os.getenv("INTERNET_CAFE_ACCOUNT", "")
  INTERNET_CAFE_PASSWORD = os.getenv("INTERNET_CAFE_PASSWORD", "")
  STAFF_CAFE_ACCOUNT = os.getenv("STAFF_CAFE_ACCOUNT", "")
  STAFF_ACCOUNT = os.getenv("STAFF_ACCOUNT", "")
  STAFF_PASSWORD = os.getenv("STAFF_PASSWORD", "")
  AGENT_ACCOUNT = os.getenv("AGENT_ACCOUNT", "")
  AGENT_PASSWORD = os.getenv("AGENT_PASSWORD", "")
