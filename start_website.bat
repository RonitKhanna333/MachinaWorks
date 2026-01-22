@echo off
echo.
echo ========================================
echo   Starting AI Consultancy Website
echo ========================================
echo.

cd /d "%~dp0\website"

echo Installing dependencies (if needed)...
call npm install

echo.
echo Starting Next.js development server...
echo Website will be available at http://localhost:3000
echo.

call npm run dev

pause
