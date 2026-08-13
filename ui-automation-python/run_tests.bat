@echo off
setlocal
cd /d "%~dp0"
call run_ui_tests.bat %*
exit /b %ERRORLEVEL%
