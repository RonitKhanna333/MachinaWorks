@echo off
echo.
echo ============================================================
echo   Starting AI Consultancy Backend
echo ============================================================
echo.

cd /d "%~dp0"

echo Using Conda Python Environment...
"C:\Users\Ronit Khanna\.conda\envs\open_manus\python.exe" src\api\server_simple.py

pause
