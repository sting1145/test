# 熊猫掌柜自动化测试 — UI + API

针对 [熊猫掌柜登录](https://passport.xiongmaozhanggui.com/account/login) 的 **UI 自动化** 与 **接口自动化**（pytest + Allure）。

## 技术栈

| 组件 | 说明 |
|------|------|
| Python 3.12 | 运行环境 |
| Selenium 4 | UI 浏览器自动化 |
| requests | 接口自动化 HTTP 客户端 |
| pytest | 测试框架 |
| Allure | HTML 测试报告 |

## 项目结构

```
ui-automation-python/
├── api/clients/              # 接口 Client
│   └── passport_client.py    # 登录等 API
├── pages/                    # UI Page Object
├── tests/
│   ├── ui/                   # UI 用例（@pytest.mark.ui）
│   │   ├── conftest.py
│   │   └── test_login.py
│   └── api/                  # 接口用例（@pytest.mark.api）
│       ├── conftest.py
│       └── test_login_sql_injection.py
├── utils/
│   ├── api_assertions.py     # 接口断言（含 SQL 注入）
│   └── sql_injection_payloads.py
└── scripts/
    ├── run_ui_tests.ps1
    └── run_api_tests.ps1
```

## 快速开始

### 1. 安装依赖

```powershell
cd C:\Users\yangjianbo\ui-automation-python

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
scripts\check_env.bat          # 检查 Python / Java / Allure
scripts\install_allure.bat     # 安装内置 Allure CLI（仅需一次）
```

> **注意**：Allure 报告需要 **Java 17+**。若未安装：
> ```powershell
> winget install Microsoft.OpenJDK.17
> ```

### 2. 配置环境

```powershell
copy .env.example .env
```

编辑 `.env` 设置 `BASE_URL`（正向用例暂不需要配置账号）。

#### 接口 Session 复用（跳过滑块登录）

1. Chrome 手动登录后，从 Network 任意已登录请求复制 **Cookie** 整行
2. 写入 `.env`：

```ini
SESSION_ACCOUNT_B=xmzg_你的账号
SESSION_COOKIE_B=panda_passport=...

# 熊猫掌柜实际接口示例
API_CURRENT_USER_PATH=/api/v1/user_info
API_LIST_PATH=/api/c1/get_jifei_conf
API_USER_REFERER=https://passport.xiongmaozhanggui.com/home
API_LIST_REFERER=https://passport.xiongmaozhanggui.com/goods/goods_list
```

3. 校验 Cookie 是否可用：

```powershell
verify_session_cookie.bat
```

4. 跑会话接口用例：

```powershell
pytest -m "api and session"
```

### 3. 运行测试

```powershell
# UI 自动化（默认 run_tests.bat 等同 run_ui_tests.bat）
run_ui_tests.bat
run_tests_and_report.bat

# 接口自动化 — 当前含登录 SQL 注入用例
run_api_tests.bat
run_api_tests_and_report.bat

# 按标记单独跑
pytest -m ui
pytest -m api
pytest -m "api and security"
pytest -m "api and session"
```

### 4. Allure 报告（中文 + 历史归档）

项目已内置 Allure CLI，**每次执行按时间戳归档，不会覆盖历史报告**。

#### 目录结构

```
reports/
├── index.html                          # 历史报告索引（所有执行记录）
├── latest-report.html                  # 最新一次报告（双击打开）
├── latest.txt                          # 最近一次运行编号
└── runs/
    └── 20260813_094600/                # 每次执行一个独立目录
        ├── meta.json                   # 执行时间、通过/失败数
        ├── allure-results/             # 原始结果 JSON
        └── report.html                 # 单文件 HTML 报告（双击打开）
```

| 脚本 | 说明 |
|------|------|
| `run_tests_and_report.bat` | **一键：测试 → 生成报告 → 打开最新报告** |
| `run_tests.bat` | 跑测试并归档到 `reports/runs/{时间戳}/` |
| `generate_report.bat [运行编号]` | 生成报告（默认最新一次） |
| `run_open_report.bat [运行编号]` | 打开指定或最新报告 |
| `run_history.bat` | 打开历史索引页 `reports/index.html` |
| `run_report.bat` | 从最新结果直接 serve（不生成 HTML） |

#### 可直接双击打开的 HTML 报告

每次生成报告后会产出**单文件 HTML**，可直接双击在浏览器中打开，**无需命令行**：

| 文件 | 说明 |
|------|------|
| `reports\latest-report.html` | 最近一次测试报告（推荐，双击打开） |
| `reports\runs\{运行编号}\report.html` | 某次历史报告（双击打开） |
| `reports\index.html` | 历史记录索引（可点击链接打开各次报告） |

```powershell
run_tests_and_report.bat   # 跑完后自动打开 latest-report.html
generate_report.bat        # 仅根据已有结果生成 HTML（不跑测试）
```

> **各页签说明**
> - **总览**：执行统计、通过率
> - **类别**：按通过/失败/跳过分类
> - **测试套**：按测试类查看全部用例（推荐）
> - **功能**：按 Epic/Feature/Story 查看用例

## 用例清单

| 分类 | 数量 | 说明 |
|------|------|------|
| 自动化负向/冒烟/安全 | 16 条 | 含 `@testcase` 装饰器，含 3 条 SQL 注入（参数化共 15 次执行） |
| 正向登录 | 3 条 | `@pytest.mark.positive`，含滑块验证码，默认跳过 |

> Session 级 `driver` 当前 13 条规模足够；若启用 `pytest-xdist` 并行或单用例搞崩浏览器，需改为 function 级 fixture。

## 环境变量

```env
BASE_URL=https://passport.xiongmaozhanggui.com
HEADLESS=false          # true 则无头模式
IMPLICIT_WAIT=10          # 已废弃，请改用 EXPLICIT_WAIT
EXPLICIT_WAIT=10          # 页面对象显式等待超时（秒）
PAGE_LOAD_TIMEOUT=30

INTERNET_CAFE_ACCOUNT=
INTERNET_CAFE_PASSWORD=
```

## 失败截图

用例在 **setup** 或 **call** 阶段失败时：

1. 自动保存到 `screenshots/{运行编号}/`
2. **同时附加到 Allure 报告**，无需再去文件夹里找

在 HTML 报告中查看路径：

- 打开 `reports/latest-report.html`
- 进入失败用例 → **附件** 区域 → 点击 **失败截图 (call)** 或 **失败截图 (setup)**
- 截图会直接内嵌在单文件报告中显示

## 会话与状态一致性（手工测试）

针对「同浏览器切换账号后右上角与数据不一致」等 SPA 状态问题，已单独整理 **15 条手工用例**：

```powershell
export_session_testcases.bat
```

生成文件：`docs/会话与状态一致性测试用例.xlsx`

| 优先级 | 建议先测 |
|--------|----------|
| P0 | TC-SESSION-001 ~ 003、007、014（账号切换、直链、接口一致） |
| P1 | 刷新、多 Tab、登出后退、localStorage 篡改兜底等 |
