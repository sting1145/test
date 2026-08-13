@echo off
setlocal
cd /d "%~dp0.."

echo [1/2] Installing Python dependencies...
if not exist ".venv\Scripts\python.exe" (
  echo [ERROR] Virtual env not found. Run setup.bat first.
  exit /b 1
)

echo [2/2] Downloading Allure CLI...
set "ALLURE_DIR=%CD%\tools\allure"
set "ALLURE_ZIP=%ALLURE_DIR%\allure.zip"
set "ALLURE_URL=https://github.com/allure-framework/allure2/releases/download/2.35.1/allure-2.35.1.zip"

if exist "%ALLURE_DIR%\allure-2.35.1\bin\allure.bat" (
  echo Allure already installed.
  exit /b 0
)

mkdir "%ALLURE_DIR%" 2>nul
powershell -NoProfile -Command "Invoke-WebRequest -Uri '%ALLURE_URL%' -OutFile '%ALLURE_ZIP%' -UseBasicParsing"
if errorlevel 1 (
  echo [ERROR] Failed to download Allure.
  exit /b 1
)

powershell -NoProfile -Command "Expand-Archive -Path '%ALLURE_ZIP%' -DestinationPath '%ALLURE_DIR%' -Force"
if errorlevel 1 (
  echo [ERROR] Failed to extract Allure.
  exit /b 1
)

echo Allure installed: %ALLURE_DIR%\allure-2.35.1\bin\allure.bat
