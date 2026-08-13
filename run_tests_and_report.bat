@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo ============================================
echo   熊猫掌柜收银台 UI 自动化 - 一键运行
echo ============================================
echo.

if not exist ".venv\Scripts\pytest.exe" (
  echo [INFO] 首次运行，正在安装环境...
  call setup.bat
  if errorlevel 1 exit /b 1
)

if not exist "tools\allure\allure-2.35.1\bin\allure.bat" (
  echo [INFO] 正在安装 Allure 报告工具...
  call scripts\install_allure.bat
  if errorlevel 1 (
    echo [ERROR] Allure 安装失败，请检查网络或手动安装 Java。
    pause
    exit /b 1
  )
)

echo.
echo [1/3] 运行测试（请确保收银台程序已启动）...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\run_tests.ps1"
set TEST_EXIT=%ERRORLEVEL%

echo.
echo [2/3] 生成 Allure HTML 报告...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\generate_report.ps1"
set REPORT_EXIT=%ERRORLEVEL%

echo.
if %TEST_EXIT% neq 0 (
  echo [WARN] 测试存在失败，退出码: %TEST_EXIT%
) else (
  echo [OK] 全部测试通过。
)

if %REPORT_EXIT% neq 0 (
  echo [ERROR] 报告生成失败。
  pause
  exit /b %REPORT_EXIT%
)

echo.
echo [3/3] 打开最新报告...
if exist "reports\latest-report.html" (
  start "" "%CD%\reports\latest-report.html"
  echo 已打开: reports\latest-report.html
) else (
  echo [WARN] 未找到报告文件。
)

echo.
echo 历史报告索引: reports\index.html
echo.
pause
exit /b %TEST_EXIT%
