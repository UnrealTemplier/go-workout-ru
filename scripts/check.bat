@echo off
call "%~dp0_lib.bat"
set "RC="
rem Всё перед коммитом: строгая сборка, строгий аудит
%PY% -m engine.build --all --strict && %PY% -m engine.audit --strict
if not defined RC set "RC=%ERRORLEVEL%"
if not defined NOPAUSE pause
exit /b %RC%
