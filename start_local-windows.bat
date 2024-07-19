@echo off
REM Change to the directory where the script is located
cd /d "%~dp0"

REM Create a virtual environment
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate

REM Install the required dependencies
pip install -r requirements.txt

REM Run the Flask application
flask run