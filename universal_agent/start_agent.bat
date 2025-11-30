@echo off
echo Starting Universal Digital Agent...
start "Universal Agent Core" python main.py
echo Core started.
echo Starting Dashboard...
start "Agent Dashboard" python ui/dashboard.py
echo Dashboard started at http://localhost:5000
echo.
echo Press any key to stop all processes...
pause
taskkill /F /IM python.exe
