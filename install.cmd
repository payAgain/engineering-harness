@echo off
REM Optional editable install so `eh` is on PATH.
setlocal
cd /d "%~dp0"
python -m pip install -e .
if errorlevel 1 exit /b %ERRORLEVEL%
echo.
echo Install OK. Try: eh --version
echo Or without install: eh.cmd --version
exit /b 0
