@echo off
REM Create venv if missing, activate it, and install requirements.txt
set VENV_DIR=%~dp0\..\lostenv
if not exist "%VENV_DIR%\Scripts\python.exe" (
    python -m venv "%VENV_DIR%"
)
call "%VENV_DIR%\Scripts\activate"
pip install --upgrade pip
pip install -r "%~dp0\..\requirements.txt"
echo Virtualenv activated and dependencies installed. Run: python manage.py runserver
