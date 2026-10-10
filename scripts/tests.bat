@echo off
call "%~dp0_lib.bat"
set "RC="
rem Тесты ядра (тесты демо-книги здесь пропускаются)
%PY% -m unittest discover -s engine/tests -t .
if not defined RC set "RC=%ERRORLEVEL%"
if not defined NOPAUSE pause
exit /b %RC%
