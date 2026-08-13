import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


class Config:
  CASHIER_BASE_URL = os.getenv("CASHIER_BASE_URL", "http://127.0.0.1:9981")
  CASHIER_SERVER_IP = os.getenv("CASHIER_SERVER_IP", "172.16.99.70")
  CASHIER_ACCOUNT = os.getenv("CASHIER_ACCOUNT", "xmzg_yjb001")
  CASHIER_PASSWORD = os.getenv("CASHIER_PASSWORD", "123456")

  HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
  BROWSER_CHANNEL = os.getenv("BROWSER_CHANNEL", "chrome")
  ACTION_TIMEOUT = int(os.getenv("ACTION_TIMEOUT", "10000"))
  NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT", "30000"))

  SCREENSHOT_DIR = ROOT_DIR / "screenshots"
