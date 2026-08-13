@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
if not exist ".venv\Scripts\python.exe" (
  echo [1/4] 创建虚拟环境...
  python -m venv .venv
)

echo [2/4] 安装 Python 依赖...
".venv\Scripts\pip.exe" install -r requirements.txt

echo [3/5] 安装 Playwright 驱动（使用本机 Chrome）...
".venv\Scripts\python.exe" -m playwright install chrome

echo [4/5] 安装 Allure 报告工具...
call scripts\install_allure.bat

if not exist ".env" (
  echo [5/5] 复制 .env.example -> .env
  copy .env.example .env
) else (
  echo [5/5] .env 已存在，跳过
)

echo.
echo 安装完成。运行测试：
echo   .venv\Scripts\activate
echo   pytest
endlocal
