@echo off
setlocal
cd /d "%~dp0"

echo ===== Step 1: Run API tests =====
call run_api_tests.bat
set TEST_EXIT=%ERRORLEVEL%

echo.
echo ===== Step 2: Generate HTML report =====
call generate_report.bat
set REPORT_EXIT=%ERRORLEVEL%

if %REPORT_EXIT% neq 0 (
  echo [ERROR] Report generation failed.
  exit /b %REPORT_EXIT%
)

echo.
if %TEST_EXIT% neq 0 (
  echo [WARN] API tests finished with failures. Exit code: %TEST_EXIT%
) else (
  echo [OK] All API tests passed.
)

if exist "reports\latest-report.html" (
  start "" "%CD%\reports\latest-report.html"
)

exit /b %TEST_EXIT%
