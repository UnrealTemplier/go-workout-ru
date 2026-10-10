@echo off
chcp 65001 >nul
set "NOPAUSE=1"
:menu
echo.
echo go-workout: команды
echo    1. check - Всё перед коммитом: строгая сборка, строгий аудит
echo    2. build - Полная сборка сайта в dist/
echo    3. build-strict - Полная сборка; предупреждения сборки — ошибки
echo    4. build-clean - Чистая пересборка: удалить dist/ и собрать заново (убирает страницы-сироты)
echo    5. build-chapter - Сборка одной главы (номер — аргументом или по запросу)
echo    6. audit - Аудит dist/: ссылки, якоря, имена файлов, ассеты, offline, диаграммы
echo    7. audit-strict - Аудит + предупреждения сборки как ошибки
echo    8. audit-full - Полный аудит: --strict и рантайм KaTeX/Mermaid в Firefox (несколько минут)
echo    9. audit-no-browser - Аудит без Firefox (без рантайм-разбора диаграмм)
echo   10. runtime-projection - Что браузер нарисовал на каждой странице (формулы, диаграммы, ошибки JS), Firefox
echo   11. tests - Тесты ядра (тесты демо-книги здесь пропускаются)
echo   12. engine-sync - Обновить engine/ из репозитория движка (ENGINE_DIR, по умолчанию ../html-textbook-engine); делает коммит
echo   13. open-site - Открыть dist/index.html в браузере
set "c="
set /p "c=Номер (Enter - выход): "
if "%c%"=="" exit /b 0
if "%c%"=="1" call "%~dp0check.bat" & goto done
if "%c%"=="2" call "%~dp0build.bat" & goto done
if "%c%"=="3" call "%~dp0build-strict.bat" & goto done
if "%c%"=="4" call "%~dp0build-clean.bat" & goto done
if "%c%"=="5" call "%~dp0build-chapter.bat" & goto done
if "%c%"=="6" call "%~dp0audit.bat" & goto done
if "%c%"=="7" call "%~dp0audit-strict.bat" & goto done
if "%c%"=="8" call "%~dp0audit-full.bat" & goto done
if "%c%"=="9" call "%~dp0audit-no-browser.bat" & goto done
if "%c%"=="10" call "%~dp0runtime-projection.bat" & goto done
if "%c%"=="11" call "%~dp0tests.bat" & goto done
if "%c%"=="12" call "%~dp0engine-sync.bat" & goto done
if "%c%"=="13" call "%~dp0open-site.bat" & goto done
echo Нет пункта %c%
:done
echo.
pause
goto menu
