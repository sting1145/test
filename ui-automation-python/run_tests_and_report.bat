@echo off
setlocal
cd /d "%~dp0"

echo ===== Step 1: Run tests (archived by timestamp) =====
call run_tests.bat
set TEST_EXIT=%ERRORLEVEL%

echo.
echo ===== Step 2: Generate HTML report =====
call generate_report.bat
set REPORT_EXIT=%ERRORLEVEL%

echo.
if %TEST_EXIT% neq 0 (
  echo [WARN] Tests finished with failures. Exit code: %TEST_EXIT%
) else (
  echo [OK] All tests passed.
)

if %REPORT_EXIT% neq 0 (
  echo [ERROR] Report generation failed.
  exit /b %REPORT_EXIT%
)

echo.
echo ===== Step 3: Open latest HTML report =====
if exist "reports\latest-report.html" (
  start "" "%CD%\reports\latest-report.html"
  echo Opened: reports\latest-report.html
) else (
  call run_open_report.bat
)

echo.
echo History index: reports\index.html
exit /b %TEST_EXIT%
