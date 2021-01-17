@echo off
For /f "tokens=2 delims=/ " %%a in ('date /t') do (set mydate=%%a)
For /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)

call venv//Scripts//activate.bat
python main.py > logs/%mydate%_%mytime%_log.txt
call venv//Scripts//deactivate.bat