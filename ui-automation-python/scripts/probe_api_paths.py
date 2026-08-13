"""临时脚本：从登录页 HTML 提取 /api/v1/ 路径（开发调试用）。"""

import re
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils.config import Config


def main() -> None:
  response = requests.get(
    f"{Config.BASE_URL}/account/login",
    timeout=Config.API_TIMEOUT,
  )
  paths = sorted(set(re.findall(r"/api/v1/[a-zA-Z0-9_/-]+", response.text)))
  print("paths in HTML:")
  for path in paths:
    print(path)


if __name__ == "__main__":
  main()
