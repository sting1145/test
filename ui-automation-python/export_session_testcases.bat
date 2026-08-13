@echo off
setlocal
cd /d "%~dp0"
.\.venv\Scripts\python.exe scripts\export_session_testcases_to_excel.py
exit /b %ERRORLEVEL%
