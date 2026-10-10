#!/usr/bin/env sh
# Меню всех команд go-workout: выберите номер, после выполнения — снова меню.
cd "$(dirname "$0")" || exit 1
while true; do
  echo ""
  echo "go-workout: команды"
  echo "   1. check — Всё перед коммитом: строгая сборка, строгий аудит"
  echo "   2. build — Полная сборка сайта в dist/"
  echo "   3. build-strict — Полная сборка; предупреждения сборки — ошибки"
  echo "   4. build-clean — Чистая пересборка: удалить dist/ и собрать заново (убирает страницы-сироты)"
  echo "   5. build-chapter — Сборка одной главы (номер — аргументом или по запросу)"
  echo "   6. audit — Аудит dist/: ссылки, якоря, имена файлов, ассеты, offline, диаграммы"
  echo "   7. audit-strict — Аудит + предупреждения сборки как ошибки"
  echo "   8. audit-full — Полный аудит: --strict и рантайм KaTeX/Mermaid в Firefox (несколько минут)"
  echo "   9. audit-no-browser — Аудит без Firefox (без рантайм-разбора диаграмм)"
  echo "  10. runtime-projection — Что браузер нарисовал на каждой странице (формулы, диаграммы, ошибки JS), Firefox"
  echo "  11. tests — Тесты ядра (тесты демо-книги здесь пропускаются)"
  echo "  12. engine-sync — Обновить engine/ из репозитория движка (ENGINE_DIR, по умолчанию ../html-textbook-engine); делает коммит"
  echo "  13. open-site — Открыть dist/index.html в браузере"
  printf "Номер (Enter — выход): "
  read -r c || exit 0
  [ -z "$c" ] && exit 0
  case "$c" in
    1) sh ./check.sh ;;
    2) sh ./build.sh ;;
    3) sh ./build-strict.sh ;;
    4) sh ./build-clean.sh ;;
    5) sh ./build-chapter.sh ;;
    6) sh ./audit.sh ;;
    7) sh ./audit-strict.sh ;;
    8) sh ./audit-full.sh ;;
    9) sh ./audit-no-browser.sh ;;
    10) sh ./runtime-projection.sh ;;
    11) sh ./tests.sh ;;
    12) sh ./engine-sync.sh ;;
    13) sh ./open-site.sh ;;
    *) echo "Нет пункта $c" ;;
  esac
  printf "\nГотово (код %s). Enter — назад в меню... " "$?"
  read -r _ || exit 0
done
