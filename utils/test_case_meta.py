"""收银台测试用例元数据：Allure 报告前置条件、步骤、测试数据。"""

from utils.config import Config

_TEST_DATA = {
  "server_ip": Config.CASHIER_SERVER_IP,
  "account": Config.CASHIER_ACCOUNT,
  "password": Config.CASHIER_PASSWORD,
}

TEST_CASES = [
  {
    "method": "test_should_load_login_page_with_core_elements",
    "title": "应正确加载登录页并展示核心元素",
    "precondition": "1. 收银台程序已启动\n2. 可访问登录页",
    "steps": "1. 打开登录页\n2. 检查页面核心元素",
    "expected": "1. 显示登录页标题与表单\n2. 显示 4 段服务器 IP 输入框",
    "data": "无",
  },
  {
    "method": "test_should_require_server_ip_account_and_password",
    "title": "服务器IP、账号和密码均为空时应提示必填",
    "precondition": "1. 收银台程序已启动\n2. 已打开登录页",
    "steps": "1. 不填写任何字段\n2. 点击登录",
    "expected": "1. 提示「请输入服务器IP」\n2. 仍停留在登录页",
    "data": "服务器IP：空\n账号：空\n密码：空",
  },
  {
    "method": "test_should_require_account_when_only_ip_filled",
    "title": "仅填写服务器IP不填账号时应提示输入账号",
    "precondition": "1. 收银台程序已启动\n2. 已打开登录页",
    "steps": "1. 填写服务器 IP\n2. 账号和密码留空\n3. 点击登录",
    "expected": "1. 提示「请输入账号」\n2. 仍停留在登录页",
    "data": f"服务器IP：{_TEST_DATA['server_ip']}\n账号：空\n密码：空",
  },
  {
    "method": "test_should_require_password_when_ip_and_account_filled",
    "title": "仅填写服务器IP和账号不填密码时应提示输入密码",
    "precondition": "1. 收银台程序已启动\n2. 已打开登录页",
    "steps": "1. 填写服务器 IP 和账号\n2. 密码留空\n3. 点击登录",
    "expected": "1. 提示「请输入密码」\n2. 仍停留在登录页",
    "data": (
      f"服务器IP：{_TEST_DATA['server_ip']}\n"
      f"账号：{_TEST_DATA['account']}\n"
      "密码：空"
    ),
  },
  {
    "method": "test_should_login_successfully_with_valid_credentials",
    "title": "使用有效服务器IP、账号和密码应登录成功",
    "precondition": "1. 收银台程序已启动\n2. 已打开登录页\n3. 测试账号可用",
    "steps": "1. 填写服务器 IP\n2. 填写账号和密码\n3. 点击登录",
    "expected": "1. 登录成功\n2. localStorage 写入 userinfo",
    "data": (
      f"服务器IP：{_TEST_DATA['server_ip']}\n"
      f"账号：{_TEST_DATA['account']}\n"
      f"密码：{_TEST_DATA['password']}"
    ),
  },
  {
    "method": "test_should_login_successfully_when_password_is_1234567",
    "title": "使用密码1234567应登录成功",
    "precondition": "1. 收银台程序已启动\n2. 已打开登录页\n3. 测试账号可用",
    "steps": "1. 填写服务器 IP\n2. 填写账号和密码\n3. 点击登录",
    "expected": "1. 登录成功\n2. localStorage 写入 userinfo",
    "data": (
      f"服务器IP：{_TEST_DATA['server_ip']}\n"
      f"账号：{_TEST_DATA['account']}\n"
      "密码：1234567"
    ),
  },
]

CASE_BY_METHOD = {item["method"]: item for item in TEST_CASES}
