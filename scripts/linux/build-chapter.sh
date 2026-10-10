#!/usr/bin/env sh
# Сборка одной главы (номер — аргументом или по запросу)
. "$(dirname "$0")/_lib.sh"
if [ $# -gt 0 ]; then V="$1"; shift; else printf "%s: " "Номер главы"; read -r V; fi
$PY -m engine.build --module "$V" "$@"
