@echo off
setlocal
cd /d "%~dp0"
.\.venv\Scripts\python.exe scripts\verify_session_cookie.py
exit /b %ERRORLEVEL%
