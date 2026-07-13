@echo off
REM Engineering Harness CLI launcher (repo root). No pip install required.
setlocal
set "FRAMEWORK_ROOT=%~dp0"
set "FRAMEWORK_ROOT=%FRAMEWORK_ROOT:~0,-1%"
set "PYTHONPATH=%FRAMEWORK_ROOT%\src;%PYTHONPATH%"
python -m engineering_harness %*
exit /b %ERRORLEVEL%
