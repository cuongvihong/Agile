@echo off
echo ========================================================
echo Opening Test Reports in Default Web Browser...
echo ========================================================

:: 1. Open Pytest HTML Report
start "" "%~dp0artifacts\reports\report.html"

:: 2. Launch Allure Preview Server and open in Browser
start "" allure open -p 52525 "%~dp0artifacts\allure-report"

echo Reports opened!
pause
