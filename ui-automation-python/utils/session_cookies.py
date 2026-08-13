"""从 .env 解析并注入 Session Cookie。"""

from urllib.parse import urlparse


def parse_cookie_header(cookie_header: str) -> dict[str, str]:
  cookies: dict[str, str] = {}
  for part in cookie_header.split(";"):
    item = part.strip()
    if not item or "=" not in item:
      continue
    name, value = item.split("=", 1)
    cookies[name.strip()] = value.strip()
  return cookies


def apply_cookies_to_session(session, base_url: str, cookie_header: str) -> dict[str, str]:
  parsed = urlparse(base_url)
  domain = parsed.hostname or ""
  cookies = parse_cookie_header(cookie_header)

  for name, value in cookies.items():
    session.cookies.set(name, value, domain=domain, path="/")

  return cookies
