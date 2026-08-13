@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\open_report.ps1" -RunId "%~1"
exit /b %ERRORLEVEL%
