# 熊猫掌柜自动化测试仓库

本仓库包含两个独立项目，互不影响：

| 目录 | 说明 | 技术栈 |
|------|------|--------|
| **根目录** | 收银台 UI 自动化 | Python + Playwright |
| **[ui-automation-python/](ui-automation-python/)** | 登录系统 UI + 接口自动化 | Python + Selenium + requests + pytest + Allure |

---

## 收银台 UI 自动化（根目录）

基于 **Python + Playwright** 的收银台 UI 自动化项目，针对本地收银台程序（`http://127.0.0.1:9981`）设计。

### 环境要求

- Python 3.10+
- 收银台程序已启动（窗口标题：收银台）

### 快速开始

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

### 配置

在 `.env` 中配置测试账号：

```env
CASHIER_BASE_URL=http://127.0.0.1:9981
CASHIER_SERVER_IP=172.16.99.70
CASHIER_ACCOUNT=xmzg_yjb001
CASHIER_PASSWORD=123456
HEADLESS=true
```

### 项目结构

```
pages/
  cashier_login_page.py   # 收银台登录页 Page Object
utils/
  cashier_auth.py         # WebSocket 握手、登录 API、路由拦截
tests/
  test_cashier_login.py   # 登录用例
```

### 一键运行（推荐）

双击项目根目录下的 `run_tests_and_report.bat`。

首次使用前双击 `setup.bat` 安装依赖。

### 报告说明

- 最新报告：`reports/latest-report.html`
- 历史索引：`reports/index.html`

---

## 登录系统 UI + 接口自动化（ui-automation-python/）

针对 [熊猫掌柜登录](https://passport.xiongmaozhanggui.com/account/login) 的 Web UI 与接口自动化。

```bash
cd ui-automation-python
setup.bat   # 或按 README 安装依赖
run_ui_tests.bat
run_api_tests.bat
```

详细说明见 [ui-automation-python/README.md](ui-automation-python/README.md)。
