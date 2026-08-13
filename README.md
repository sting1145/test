# UI Automation Cashier — 熊猫掌柜收银台

基于 **Python + Playwright** 的收银台 UI 自动化项目，针对本地收银台程序（`http://127.0.0.1:9981`）设计。

## 环境要求

- Python 3.10+
- 收银台程序已启动（窗口标题：收银台）

## 快速开始

```bash
setup.bat
.venv\Scripts\activate
pytest
```

或手动安装：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chrome
copy .env.example .env
pytest
```

本项目默认使用 **本机已安装的 Google Chrome**（`BROWSER_CHANNEL=chrome`），一般不需要下载 Playwright 自带的 Chromium。

若本机没有 Chrome，可改为 Edge：`BROWSER_CHANNEL=msedge`，并执行 `python -m playwright install msedge`。

若仍报浏览器不存在，再执行：

```bash
python -m playwright install chromium
```

## 配置

在 `.env` 中配置测试账号：

```env
CASHIER_BASE_URL=http://127.0.0.1:9981
CASHIER_SERVER_IP=172.16.99.70
CASHIER_ACCOUNT=xmzg_yjb001
CASHIER_PASSWORD=123456
HEADLESS=true
```

## 项目结构

```
pages/
  cashier_login_page.py   # 收银台登录页 Page Object
utils/
  cashier_auth.py         # WebSocket 握手、登录 API、路由拦截
tests/
  test_cashier_login.py   # 登录用例
```

## 一键运行（推荐）

**双击**项目根目录下的：

```
run_tests_and_report.bat
```

会自动：运行测试 → 生成 Allure 报告 → 打开 HTML 报告。

首次使用前双击 `setup.bat` 安装依赖。

## 测试用例（6 条）

| 分类 | 用例 |
|------|------|
| 页面加载 | 应正确加载登录页并展示核心元素 |
| 表单校验 | IP/账号/密码为空等 3 条校验 |
| 正向登录 | 密码 `123456` 登录成功 |
| 负向登录 | 密码 `1234567` 登录失败 |

## 报告说明

- 最新报告：`reports/latest-report.html`（双击打开）
- 历史索引：`reports/index.html`
- 失败用例自动截图，附在 Allure 报告中

## 手动运行

```bash
# 运行全部用例
pytest

# 只跑正向登录
pytest -m positive

# 有界面调试
set HEADLESS=false
pytest -m positive

# 只跑登录相关
pytest -m login
```

## 技术说明

收银台是 CEF 内嵌 Web 应用。登录流程依赖：

1. WebSocket 获取 `token/nid`（`172.16.99.70:16510`）
2. 云端登录 API
3. 页面内 `to_browser` 握手

测试通过 Playwright 拦截登录 API、模拟握手，并校验 `localStorage.userinfo` 写入成功。

## 为什么用 Playwright 而不是 Selenium

本项目选用 **Playwright**，因为：

- 原生支持 `page.route()` 拦截请求（绕过浏览器 CORS）
- 与现有 TypeScript 版收银台自动化方案一致
- 对本地 `127.0.0.1:9981` 页面支持更好

如需 Selenium 版本，可将 Page Object 中的定位器迁移到 `selenium.webdriver`，但登录 API 拦截需改用其他方式（如代理或直接在页面注入响应）。
