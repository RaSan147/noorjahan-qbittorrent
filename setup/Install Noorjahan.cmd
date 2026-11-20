@echo off
rem Runs install.ps1 next to this file. Installs Inter for this user and copies the themes.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1"
echo.
pause
