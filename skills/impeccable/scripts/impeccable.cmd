@echo off
setlocal
powershell.exe -NoProfile -File "%~dp0impeccable.ps1" %*
exit /b %errorlevel%
