DAILY BACKUP FOLDER
===================

This folder contains automatic daily JSON backups of the ERP system.

- Files are named: auto_backup_YYYYMMDD_HHMMSS.json
- Maximum 30 backups are kept (oldest deleted automatically)
- Backups include: Settings, Employees, IGP, VGP, MGP, Help Desk, Grievance

To run a manual backup:
  Z:\myenv\Scripts\python.exe manage.py auto_backup

To schedule via Windows Task Scheduler:
  Program : Z:\myenv\Scripts\python.exe
  Arguments: "Z:\erp system\manage.py" auto_backup
  Start in : Z:\erp system
  Trigger  : Daily at 00:00
