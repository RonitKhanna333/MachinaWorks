@echo off
echo.
echo ============================================================
echo   Starting Complete AI Consultancy System
echo ============================================================
echo.
echo This will start:
echo   1. Python Backend API (Port 8000)
echo   2. Next.js Website (Port 3000)
echo.
echo Press any key to start both servers...
pause > nul

cd /d "%~dp0"

echo.
echo [1/2] Starting Backend API...
start "AI Consultancy Backend" cmd /k "conda activate open_manus && python src/api/server.py"

timeout /t 5 /nobreak > nul

echo [2/2] Starting Website...
start "AI Consultancy Website" cmd /k "cd website && npm run dev"

echo.
echo ============================================================
echo   Both servers are starting!
echo ============================================================
echo.
echo Backend API:  http://localhost:8000
echo API Docs:     http://localhost:8000/docs
echo Website:      http://localhost:3000
echo.
echo Press any key to open the website in your browser...
pause > nul

start http://localhost:3000

echo.
echo System is running! Close this window to stop all servers.
pause
