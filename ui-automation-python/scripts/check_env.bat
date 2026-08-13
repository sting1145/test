@echo off
setlocal
cd /d "%~dp0.."

set "OK=1"

echo Checking environment...

where java >nul 2>&1
if errorlevel 1 (
  echo [FAIL] Java not found. Allure requires JDK 17+.
  echo        Install: winget install Microsoft.OpenJDK.17
  set "OK=0"
) else (
  echo [OK]   Java
)

if not exist ".venv\Scripts\python.exe" (
  echo [FAIL] Python venv not found. Run: python -m venv .venv
  set "OK=0"
) else (
  echo [OK]   Python venv
)

if not exist "tools\allure\allure-2.35.1\bin\allure.bat" (
  echo [WARN] Allure CLI not installed. Run: scripts\install_allure.bat
) else (
  echo [OK]   Allure CLI
)

if %OK%==0 exit /b 1
echo All checks passed.
