@echo off
title Unity Cement - Daily Backup
echo.
echo  =====================================================
echo    Unity Cement ERP - Daily Backup
echo  =====================================================
echo.

cd /d "Z:\erp system"
"Z:\erp system\venv\Scripts\python.exe" manage.py auto_backup

if errorlevel 1 (
    echo.
    echo  ERROR: Backup failed. Check venv and database.
    pause
) else (
    echo.
    echo  Backup saved to: Z:\erp system\backups\
)
