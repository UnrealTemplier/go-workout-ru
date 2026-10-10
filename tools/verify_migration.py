"""
tools/verify_migration.py — проверка полноты миграции go-workout (анализ § 7.6, проверки 1, 2, 3, 5).

Сравнивает дерево Markdown (sources/) с исходными данными старого генератора, не доверяя мигратору:
  1. Структура: 100 глав, 369 разделов, 369 «00. О разделе.md», 100 «000. О главе.md», 7 666 задач;
     состав задач каждого раздела равен его диапазону.
  2. Данные: H1 раздела равен исходному названию; описания разделов, hero и итоговый блок глав на месте; каждый
     code_blocks[].code (без обрамляющих переводов строк) встречается в Markdown побайтно; каждое непустое
     поле задачи перенесено (по словам, после снятия экранирования).
  3. Условие (U15): ни одно предложение из task и из краткой формулировки не потеряно.
  5. gofmt -e для всех блоков Go (если gofmt доступен; --no-gofmt — пропустить).

Проверка 4 (видимый текст старой карточки и новой страницы) — tools/compare_visible.py после сборки.

Запуск из корня go-workout: python3 tools/verify_migration.py [--sources sources] [--no-gofmt]
Код возврата 0 — всё сошлось.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import migrate_to_md as M  # noqa: E402


def unescape_md(text):
    """Markdown мигратора → текст, сравнимый с исходными данными."""
    t = text.replace("\\(", "$").replace("\\)", "$")
    t = re.sub(r"\\([\\`*_{}\[\]()>#+\-.!])", r"\1", t)
    t = re.sub(r"&lt;(?=[A-Za-z/!?])", "<", t)
    return re.sub(r"&amp;(?=#?[A-Za-z0-9]+;)", "&", t)


def restore_source(text):
    """Исходный текст с восстановленными командами LaTeX (U25), как его должен содержать Markdown."""
    text = text.replace("\r\n", "\\r\\n").replace("\x1b", "\\x1b")
    for ch, letter in M.CTRL.items():
        text = text.replace(ch, "\\" + letter)
    return re.sub(r"\n(?=(?:e|eq|abla|u|ot|ewline)\b)", lambda m: "\\n", text) if "$" in text else text


def words(text):
    """Слова без знаков и подчёркиваний: экранирование Markdown и разметка на сравнение не влияют."""
    return re.findall(r"[^\W_]+", text.lower())


def contains_words(haystack_words, needle_words):
    """needle — подпоследовательность haystack (слова по порядку, допускаются вставки)."""
    it = iter(haystack_words)
    return all(any(w == h for h in it) for w in needle_words)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Проверка полноты миграции go-workout")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--sources", default="sources")
    ap.add_argument("--no-gofmt", action="store_true")
    args = ap.parse_args(argv)
    repo, src = args.repo, os.path.join(args.repo, args.sources)
    tasks = M.load_tasks(repo)
    meta = M.load_meta(repo, tasks)
    topics, _ = M.load_portal(repo)
    statements = M.load_statements(repo)
    problems = []

    # ---- 1. структура
    chapters = sorted(d for d in os.listdir(src) if os.path.isdir(os.path.join(src, d)))
    n_sections = n_tasks = n_sec_index = n_ch_index = 0
    files_by_chapter = {}
    for ch_dir in chapters:
        n = int(ch_dir.split(".")[0])
        ch_path = os.path.join(src, ch_dir)
        if os.path.isfile(os.path.join(ch_path, "000. О главе.md")):
            n_ch_index += 1
        secs = sorted(d for d in os.listdir(ch_path) if os.path.isdir(os.path.join(ch_path, d)))
        if len(secs) != len(meta[n]["sections"]):
            problems.append(f"глава {n}: разделов {len(secs)}, ожидалось {len(meta[n]['sections'])}")
        files_by_chapter[n] = {}
        for si, sec_dir in enumerate(secs, 1):
            n_sections += 1
            sec_path = os.path.join(ch_path, sec_dir)
            sec = meta[n]["sections"][si - 1]
            idx = os.path.join(sec_path, "00. О разделе.md")
            if os.path.isfile(idx):
                n_sec_index += 1
                text = open(idx, encoding="utf-8").read()
                if text.split("\n", 1)[0] != "# " + sec["title"]:
                    problems.append(f"{ch_dir}/{sec_dir}: H1 раздела не равен исходному названию")
                if sec["desc"] and unescape_md(text.split("\n", 2)[2].strip()) != sec["desc"]:
                    problems.append(f"{ch_dir}/{sec_dir}: описание раздела изменилось")
            else:
                problems.append(f"{ch_dir}/{sec_dir}: нет 00. О разделе.md")
            nums = []
            for f in sorted(os.listdir(sec_path)):
                m = re.match(r"^(\d{3})\. .+\.md$", f)
                if m:
                    nums.append(int(m.group(1)))
                    files_by_chapter[n][int(m.group(1))] = os.path.join(sec_path, f)
                    n_tasks += 1
            if nums != list(range(sec["start"], sec["end"] + 1)):
                problems.append(f"{ch_dir}/{sec_dir}: задачи {nums[:3]}…, ожидался диапазон {sec['start']}–{sec['end']}")
    counts = (len(chapters), n_sections, n_sec_index, n_ch_index, n_tasks)
    if counts != (100, 369, 369, 100, 7666):
        problems.append(f"структура: глав, разделов, «О разделе», «О главе», задач = {counts}")

    # ---- 2–3. данные и условие
    code_total = code_found = 0
    go_blocks = []
    for n in sorted(tasks):
        ch_dir = next(d for d in chapters if int(d.split(".")[0]) == n)
        hero = open(os.path.join(src, ch_dir, "000. О главе.md"), encoding="utf-8").read()
        hero_plain = unescape_md(hero)
        for key in ("hero_title", "hero_tag", "hero_desc"):
            if meta[n][key] not in hero_plain:
                problems.append(f"глава {n}: нет {key}")
        foot = meta[n]["footer"] or {}
        for part in [foot.get("badge", ""), foot.get("title", "")] + foot.get("paras", []):
            if part and not contains_words(words(hero), words(part)):
                problems.append(f"глава {n}: итоговый блок перенесён не полностью: {part[:40]}")
        for t in tasks[n]:
            path = files_by_chapter[n].get(t["num"])
            if not path:
                problems.append(f"глава {n}, задача {t['num']}: нет файла")
                continue
            md = open(path, encoding="utf-8").read()
            if md.split("\n", 1)[0] != "# " + t["title"]:
                problems.append(f"{path}: H1 не равен названию задачи")
            md_words = words(md)
            for cb in t.get("code_blocks") or []:
                code_total += 1
                code = cb["code"].strip("\n")
                if code in md:
                    code_found += 1
                else:
                    problems.append(f"{path}: блок кода «{cb.get('filename', '')}» не найден побайтно")
                if (cb.get("lang") or "go") == "go" and not re.search(r"go\.(mod|sum|work)$", cb.get("filename") or ""):
                    go_blocks.append((path, code))
            for f, _ in M.TEXT_FIELDS:
                v = t.get(f)
                if not v or f == "code_blocks":
                    continue
                if f == "test_cases":
                    raw = " ".join(str(x) for c in v for x in c.values())
                else:
                    raw = restore_source(M.field_text(v))
                if not contains_words(md_words, words(raw)):
                    problems.append(f"{path}: поле {f} перенесено не полностью")
            st = statements[n]["items"].get(t["num"])
            if st is not None and not contains_words(md_words, words(st)):
                problems.append(f"{path}: краткая формулировка (U15) потеряна")

    # ---- 5. gofmt
    gofmt_failed = 0
    gofmt = shutil.which("gofmt")
    if args.no_gofmt or not gofmt:
        print("gofmt: пропущено" + ("" if args.no_gofmt else " (gofmt не найден)"))
    else:
        with tempfile.TemporaryDirectory() as tmp:
            for i, (path, code) in enumerate(go_blocks):
                p = os.path.join(tmp, f"b{i}.go")
                with open(p, "w", encoding="utf-8") as fp:
                    fp.write(code + "\n")
            res = subprocess.run([gofmt, "-e", "-l", tmp], capture_output=True, text=True)
            bad = {}
            for line in res.stderr.splitlines():
                m = re.match(r".*/b(\d+)\.go:", line)
                if m:
                    bad[int(m.group(1))] = line.split(": ", 1)[-1]
            gofmt_failed = len(bad)
            for i, msg in sorted(bad.items())[:20]:
                problems.append(f"gofmt -e: {go_blocks[i][0]}: {msg}")
    print(f"структура: глав {counts[0]}, разделов {counts[1]}, «О разделе» {counts[2]}, «О главе» {counts[3]}, задач {counts[4]}")
    print(f"блоков кода найдено побайтно: {code_found} из {code_total}; блоков Go: {len(go_blocks)}, gofmt -e с ошибкой: {gofmt_failed}")
    for p in problems[:60]:
        print("ПРОВАЛ " + p)
    if len(problems) > 60:
        print(f"… и ещё {len(problems) - 60}")
    print("ПРОВЕРКА ПРОЙДЕНА" if not problems else f"ПРОБЛЕМ: {len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
