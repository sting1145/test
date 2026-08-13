import hashlib
import json
import random
from dataclasses import dataclass
from typing import Any

import requests

from utils.session_cookies import apply_cookies_to_session


@dataclass
class ApiResponse:
  status_code: int
  text: str
  headers: dict

  def json(self):
    return json.loads(self.text)


class PassportClient:
  LOGIN_PATH = "/api/v1/login"
  LOGOUT_PATH = "/api/v1/logout"
  LOGIN_PAGE_PATH = "/account/login"

  def __init__(self, base_url: str, timeout: int = 30):
    self.base_url = base_url.rstrip("/")
    self.timeout = timeout
    self.session = requests.Session()
    self.session.headers.update(
      {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": self.base_url,
        "Referer": f"{self.base_url}{self.LOGIN_PAGE_PATH}",
        "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"
        ),
      }
    )

  def warm_session(self) -> None:
    """访问登录页，获取 panda_passport 等 Cookie。"""
    self.session.get(f"{self.base_url}{self.LOGIN_PAGE_PATH}", timeout=self.timeout)

  def load_cookie_header(self, cookie_header: str) -> None:
    apply_cookies_to_session(self.session, self.base_url, cookie_header)

  def set_referer(self, referer: str) -> None:
    self.session.headers["Referer"] = referer

  def request(
    self,
    method: str,
    path: str,
    *,
    base_url: str | None = None,
    params: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
  ) -> ApiResponse:
    root = (base_url or self.base_url).rstrip("/")
    response = self.session.request(
      method=method.upper(),
      url=f"{root}{path}",
      params=params,
      data=data,
      json=json_body,
      headers=headers,
      timeout=self.timeout,
    )
    api_response = ApiResponse(
      status_code=response.status_code,
      text=response.text,
      headers=dict(response.headers),
    )
    self._last_response = api_response
    return api_response

  def get(self, path: str, **kwargs) -> ApiResponse:
    return self.request("GET", path, **kwargs)

  def post(self, path: str, **kwargs) -> ApiResponse:
    return self.request("POST", path, **kwargs)

  def logout(self) -> ApiResponse:
    return self.post(self.LOGOUT_PATH)

  def login(
    self,
    user_name: str,
    password: str,
    *,
    captcha: str = "",
    hash_password: bool = True,
  ) -> ApiResponse:
    payload_password = (
      hashlib.md5(password.encode("utf-8")).hexdigest() if hash_password else password
    )
    response = self.session.post(
      f"{self.base_url}{self.LOGIN_PATH}",
      params={"r": random.random()},
      data={
        "user_name": user_name,
        "password": payload_password,
        "captcha": captcha,
      },
      timeout=self.timeout,
    )
    return ApiResponse(
      status_code=response.status_code,
      text=response.text,
      headers=dict(response.headers),
    )
