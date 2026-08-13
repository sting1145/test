@echo off
setlocal
set "ROOT=%~dp0.."
set "ALLURE_BAT=%ROOT%\tools\allure\allure-2.35.1\bin\allure.bat"
set "ALLURE_LANG=zh"

if not exist "%ALLURE_BAT%" (
  echo [ERROR] Allure CLI not found: %ALLURE_BAT%
  echo Please run: scripts\install_allure.bat
  exit /b 1
)

"%ALLURE_BAT%" %*
