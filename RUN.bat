@echo off
title Unity Cement - ERP System
color 1F
echo.
echo  =====================================================
echo    Unity Cement ERP System
echo    Starting on Local Network...
echo  =====================================================
echo.

cd /d "Z:\erp system"

echo  [1/4] Activating virtual environment...
call "Z:\erp system\venv\Scripts\activate.bat"

echo  [2/4] Running makemigrations...
"Z:\erp system\venv\Scripts\python.exe" manage.py makemigrations

echo  [3/4] Applying migrations...
"Z:\erp system\venv\Scripts\python.exe" manage.py migrate

echo  [4/4] Starting server...
echo.
echo  =====================================================
echo   THIS PC  : http://127.0.0.1:8000
echo   NETWORK  : http://192.168.113.161:8000
echo   Press CTRL+C to stop
echo  =====================================================
echo.

"Z:\erp system\venv\Scripts\python.exe" manage.py runserver 0.0.0.0:8000
pause
