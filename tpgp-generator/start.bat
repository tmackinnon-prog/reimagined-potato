@echo off
REM Launches the TPGP Generator locally and opens it in your browser.
cd /d "%~dp0"

python -c "import flask" 2>NUL
if errorlevel 1 (
  echo Installing dependencies (first run only)...
  pip install -r requirements.txt
)

if "%TPGP_PORT%"=="" (set TPGP_PORT=8200)
echo Starting TPGP Generator at http://127.0.0.1:%TPGP_PORT% ...
start "" http://127.0.0.1:%TPGP_PORT%
python app.py

pause
