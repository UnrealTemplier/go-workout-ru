@echo off
chcp 65001 >nul
title go-workout: REBUILD_ALL
rem REBUILD_ALL - полная проверка и пересборка go-workout одним запуском: зависимости, версия движка,
rem тесты ядра, чистая пересборка локального сайта dist/ и его строгий аудит с рантаймом KaTeX и Mermaid в Firefox.
rem Двойной щелчок оставляет окно открытым до закрытия пользователем.
cd /d "%~dp0.."
set "PY=py -3"
where py >nul 2>nul || set "PY=python"
set "FAILED=0"
set "NOTE="

echo.
echo ==== 1/5 Зависимости (requirements.txt)
%PY% -m pip install -q -r requirements.txt
if errorlevel 1 (set "R1=ОШИБКА" & set "FAILED=1") else (set "R1=OK")

echo.
echo ==== 2/5 Версия движка
call :engine_version
set "R2=OK"

echo.
echo ==== 3/5 Тесты ядра
%PY% -m unittest discover -s engine/tests -t .
if errorlevel 1 (set "R3=ОШИБКА" & set "FAILED=1") else (set "R3=OK")

echo.
echo ==== 4/5 Чистая пересборка сайта (dist/, локальная версия)
if exist dist rmdir /s /q dist
%PY% -m engine.build --all --strict
if errorlevel 1 (set "R4=ОШИБКА" & set "FAILED=1") else (set "R4=OK")

echo.
echo ==== 5/5 Строгий аудит и рантайм KaTeX/Mermaid в Firefox
if "%R4%"=="OK" (
  %PY% -m engine.audit --strict --katex-runtime
  if errorlevel 1 (set "R5=ОШИБКА" & set "FAILED=1") else (set "R5=OK")
) else (
  set "R5=ПРОПУЩЕНО - сборка не прошла"
)

echo.
echo ==== Итог
echo   1. Зависимости: %R1%
echo   2. Версия движка: %R2%
echo   3. Тесты ядра: %R3%
echo   4. Чистая пересборка сайта: %R4%
echo   5. Строгий аудит и рантайм: %R5%
if defined NOTE echo   ВНИМАНИЕ: %NOTE%
if "%FAILED%"=="0" (echo Всё прошло.) else (echo Есть ошибки - см. вывод шагов выше.)

echo.
rem Двойной щелчок: окно остаётся открытым, пока его не закроет пользователь
echo %CMDCMDLINE% | find /i " /c" >nul && (echo Введите exit или закройте окно. & cmd /k)
exit /b %FAILED%

:engine_version
if not exist "..\html-textbook-engine\engine\VERSION" (
  echo Репозиторий движка ..\html-textbook-engine не найден - сверка версии пропущена.
  exit /b 0
)
set "BOOK_V="
set "ENGINE_V="
set /p BOOK_V=<engine\VERSION
set /p ENGINE_V=<..\html-textbook-engine\engine\VERSION
echo Движок в книге: %BOOK_V%; в репозитории движка: %ENGINE_V%
if not "%BOOK_V%"=="%ENGINE_V%" set "NOTE=версии движка различаются: обновите engine\ через scripts\windows\engine-sync.bat"
exit /b 0
