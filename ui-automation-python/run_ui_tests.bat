@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\run_ui_tests.ps1" %*
exit /b %ERRORLEVEL%
