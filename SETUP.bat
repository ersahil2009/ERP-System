@echo off
title Unity Cement - ERP Setup
color 2F
echo.
echo  =====================================================
echo    Unity Cement ERP System - First Time Setup
echo  =====================================================
echo.

cd /d "Z:\erp system"

echo  [1/5] Activating virtual environment...
call "Z:\erp system\venv\Scripts\activate.bat"
if errorlevel 1 (
    echo  ERROR: venv not found at Z:\erp system\venv
    pause
    exit /b
)

echo  [2/5] Upgrading pip...
"Z:\erp system\venv\Scripts\python.exe" -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org

echo  [3/5] Installing dependencies...
"Z:\erp system\venv\Scripts\python.exe" -m pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
if errorlevel 1 (
    echo.
    echo  ERROR: pip install failed. Trying with --no-cache-dir...
    "Z:\erp system\venv\Scripts\python.exe" -m pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --no-cache-dir
    if errorlevel 1 (
        echo  ERROR: Installation failed. Check internet connection.
        pause
        exit /b
    )
)

echo  [4/5] Running makemigrations...
"Z:\erp system\venv\Scripts\python.exe" manage.py makemigrations accounts
"Z:\erp system\venv\Scripts\python.exe" manage.py makemigrations internal_pass
"Z:\erp system\venv\Scripts\python.exe" manage.py makemigrations visitor_pass
"Z:\erp system\venv\Scripts\python.exe" manage.py makemigrations material_pass
"Z:\erp system\venv\Scripts\python.exe" manage.py makemigrations helpdesk
"Z:\erp system\venv\Scripts\python.exe" manage.py makemigrations grievance
"Z:\erp system\venv\Scripts\python.exe" manage.py makemigrations dashboard
"Z:\erp system\venv\Scripts\python.exe" manage.py makemigrations work_permit

echo  [5/5] Applying migrations...
"Z:\erp system\venv\Scripts\python.exe" manage.py migrate --run-syncdb

echo.
echo  =====================================================
echo    Setup Complete! Run RUN.bat to start the server.
echo  =====================================================
echo.
pause
