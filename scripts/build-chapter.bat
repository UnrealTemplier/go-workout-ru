@echo off
call "%~dp0_lib.bat"
set "RC="
rem Сборка одной главы (номер — аргументом или по запросу)
set "V=%~1"
if "%V%"=="" set /p "V=Номер главы: "
%PY% -m engine.build --module %V%
if not defined RC set "RC=%ERRORLEVEL%"
if not defined NOPAUSE pause
exit /b %RC%
