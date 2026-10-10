#!/usr/bin/env sh
# Всё перед коммитом: строгая сборка, строгий аудит
. "$(dirname "$0")/_lib.sh"
$PY -m engine.build --all --strict && $PY -m engine.audit --strict
