@echo off
REM Compatibility wrapper — prefer root eh.cmd
call "%~dp0..\eh.cmd" %*
exit /b %ERRORLEVEL%
