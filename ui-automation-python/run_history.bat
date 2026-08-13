@echo off
setlocal
cd /d "%~dp0"
start "" "%CD%\reports\index.html"
echo Opened history index: reports\index.html
