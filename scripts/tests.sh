#!/usr/bin/env sh
# Тесты ядра (тесты демо-книги здесь пропускаются)
. "$(dirname "$0")/_lib.sh"
$PY -m unittest discover -s engine/tests -t .
