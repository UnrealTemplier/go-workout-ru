"""
tools/compare_visible.py — проверка 4 анализа § 7.6: видимый текст старой карточки и новой страницы.

Для каждой задачи берётся карточка #ex-N из старой страницы главы (закоммиченный dist/ старого
генератора или его копия) и <article> новой страницы задачи из сборки движка. Текст без разметки
делится на слова (знаки препинания, подчёркивания и оформление не учитываются).

  * Каждое слово старой карточки обязано найтись в новой странице в том же порядке. Пропуск — провал.
  * Слова, которые есть только на новой странице, раскладываются по классам: поля, которые старый
    сайт не показывал (best_practices, self_check, test_cases, interview_qa), исходная формулировка (U15),
    заголовки разделов страницы, восстановленные команды LaTeX (U25). Необъяснённые слова — провал.

Запуск из корня go-workout после сборки:
  python3 tools/compare_visible.py --old dist --new /tmp/dist-new [--chapters 1,23] [--report отчёт.md]
Код возврата 0 — пропусков и необъяснённых слов нет.
"""

import argparse
import collections
import difflib
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import migrate_to_md as M  # noqa: E402

CARD_END = re.compile(r'<div class="exercise-card"|<div class="section-header"|<div class="section-separator"|<section class="chapter-footer"|<script|</main>|🎉 Поздравляем')
OLD_CHROME = [
    re.compile(r'<div class="exercise-num-badge">.*?</div>', re.S),
    re.compile(r'<div class="callout-title">.*?</div>', re.S),
    re.compile(r"<h4[^>]*>.*?</h4>", re.S),
    re.compile(r"<button[^>]*>.*?</button>", re.S),
    re.compile(r'<span style="color: #38bdf8; font-weight: 700;">\d+\.</span>'),   # номер строки-пункта
]
NEW_CHROME = [
    re.compile(r"<h2[^>]*>.*?</h2>", re.S),
    re.compile(r'<header class="code-header">.*?</header>', re.S),
]
NEW_HEADINGS = ("Условие", "Теория", "Решение по шагам", "Код решения", "Под капотом", "Подводные камни",
                "На собеседовании", "Лучшие практики", "Самопроверка", "Тест-кейсы", "Исходная формулировка",
                "Вход", "Ожидается", "Вопрос с собеседования", "Ответ")
NEW_FIELDS = ("best_practices", "self_check", "test_cases", "interview_qa")


def words(text):
    return re.findall(r"[^\W_]+", text.lower())


def plain(fragment):
    out = []
    for part in re.split(r"(<pre[^>]*>.*?</pre>)", fragment, flags=re.S):
        text = html.unescape(re.sub(r"<[^>]+>", " ", part))
        if not part.startswith("<pre"):
            # вне кода старый сайт показывал испорченные команды LaTeX как есть (U25): CR + «ightarrow»
            for ch, letter in M.CTRL.items():
                text = text.replace(ch, "\\" + letter)
            text = text.replace("\x1b", "\\x1b")
        out.append(text)
    return " ".join(out)


def old_cards(path):
    with open(path, encoding="utf-8") as fp:
        page = fp.read()
    cards = {}
    for m in re.finditer(r'<div class="exercise-card" id="ex-(\d+)">', page):
        rest = page[m.end():]
        end = CARD_END.search(rest)
        frag = rest[:end.start()] if end else rest
        for rx in OLD_CHROME:
            frag = rx.sub(" ", frag)
        cards[int(m.group(1))] = words(plain(frag))
    return cards


def new_page(path):
    with open(path, encoding="utf-8") as fp:
        page = fp.read()
    h1 = re.search(r'<h1 class="article-title">(.*?)</h1>', page, re.S).group(1)
    a = page.index('<div class="article-markdown">')
    end = min(i for i in (page.find("</article>", a), page.find('<nav class="article-bottom-nav"', a)) if i > 0)
    body = page[a:end]
    for rx in NEW_CHROME:
        body = rx.sub(" ", body)
    return words(plain(h1 + " " + body))


def index_new(dist):
    """(глава, задача) → путь новой страницы: номера берутся из префиксов каталогов и файлов."""
    res = {}
    docs = os.path.join(dist, "docs")
    for ch in os.listdir(docs):
        n = int(ch.split("-")[0])
        for sec in os.listdir(os.path.join(docs, ch)):
            sp = os.path.join(docs, ch, sec)
            if not os.path.isdir(sp):
                continue
            for f in os.listdir(sp):
                k = int(f.split("-")[0])
                if k:
                    res[(n, k)] = os.path.join(sp, f)
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description="Проверка 4 § 7.6: видимый текст старых карточек и новых страниц")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--old", default="dist", help="каталог старого сайта (страницы глав NNN-*.html)")
    ap.add_argument("--new", required=True, help="каталог сборки движка")
    ap.add_argument("--chapters", help="номера глав через запятую (по умолчанию все)")
    ap.add_argument("--report")
    args = ap.parse_args(argv)
    tasks = M.load_tasks(args.repo)
    statements = M.load_statements(args.repo)
    pages = index_new(args.new)
    old_files = {int(f.split("-")[0]): os.path.join(args.old, f) for f in os.listdir(args.old)
                 if re.match(r"\d{3}-.*\.html$", f)}
    chapters = [int(x) for x in args.chapters.split(",")] if args.chapters else sorted(tasks)
    heading_words = collections.Counter(w for h in NEW_HEADINGS for w in words(h))
    stats = collections.Counter()
    failures = []
    for n in chapters:
        cards = old_cards(old_files[n])
        for t in tasks[n]:
            k = t["num"]
            stats["задач"] += 1
            old = cards.get(k)
            new = new_page(pages[(n, k)]) if (n, k) in pages else None
            if old is None or new is None:
                failures.append(f"глава {n}, задача {k}: нет {'старой карточки' if old is None else 'новой страницы'}")
                continue
            sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
            missing, added = [], collections.Counter()
            for op, a1, a2, b1, b2 in sm.get_opcodes():
                if op in ("delete", "replace"):
                    missing += old[a1:a2]
                if op in ("insert", "replace"):
                    added.update(new[b1:b2])
            # U25: старый сайт терял букву команды вместе с управляющим символом («ightarrow»), новый — «rightarrow»
            rest = []
            for w in missing:
                fix = next((l + w for l in "rtabfvn" if added[l + w] > 0), None)
                if fix:
                    added[fix] -= 1
                    stats["U25: команда LaTeX восстановлена"] += 1
                else:
                    rest.append(w)
            missing = rest
            if missing:
                # [текст](https://…): старый сайт печатал адрес текстом, теперь он в href ссылки
                urls = collections.Counter(w for f, _ in M.TEXT_FIELDS if isinstance(t.get(f), str)
                                           for u in re.findall(r"\]\((https?://[^)\s]+)\)", t[f]) for w in words(u))
                left = collections.Counter(missing) - urls
                if left != collections.Counter(missing):
                    stats["адрес ссылки ушёл в href"] += 1
                missing = list(left.elements())
            if missing:
                failures.append(f"глава {n}, задача {k}: на новой странице нет слов старой карточки: "
                                + " ".join(missing[:12]))
                stats["задач с пропусками"] += 1
            # объяснение добавленных слов
            budget = collections.Counter()
            for f in NEW_FIELDS:
                v = t.get(f)
                if v:
                    src = " ".join(str(x) for c in v for x in (c.values() if isinstance(c, dict) else [c])) \
                        if isinstance(v, list) else str(v)
                    budget.update(words(src))
                    stats[f"поле {f} показано впервые"] += 1
            st = statements[n]["items"].get(k)
            if st:
                budget.update(words(st))
            budget.update({w: 99 for w in heading_words})
            budget.update({w: 99 for w in ("r", "t", "a", "b", "f", "v", "n", "x1b", "rightarrow", "times", "text")})
            unexplained = added - budget
            numbers = [w for w in unexplained if w.isdigit() and len(w) <= 3]
            if numbers:
                # строка «2. …» внутри абзаца: старый сайт рисовал номер отдельным span (он вырезан как оформление)
                stats["номер пункта виден текстом"] += 1
                for w in numbers:
                    del unexplained[w]
            if unexplained:
                stats["задач с необъяснёнными словами"] += 1
                failures.append(f"глава {n}, задача {k}: необъяснённые слова новой страницы: "
                                + " ".join(list(unexplained.elements())[:12]))
            stats["слов старых карточек"] += len(old)
            stats["слов, добавленных на новых страницах"] += sum(added.values())
    for k, v in sorted(stats.items()):
        print(f"{k}: {v}")
    for f in failures[:40]:
        print("ПРОВАЛ " + f)
    if len(failures) > 40:
        print(f"… и ещё {len(failures) - 40}")
    if args.report:
        with open(args.report, "w", encoding="utf-8") as fp:
            fp.write("# Проверка 4: видимый текст старых карточек и новых страниц\n\n"
                     "Сгенерирован `python3 tools/compare_visible.py`; вручную не править.\n\n"
                     "| Счётчик | Значение |\n|---|--:|\n")
            for k, v in sorted(stats.items()):
                fp.write(f"| {k} | {v} |\n")
            fp.write(f"\nПровалов: {len(failures)}.\n")
            for f in failures:
                fp.write(f"\n* {f}")
            fp.write("\n")
    print("ПРОВЕРКА ПРОЙДЕНА" if not failures else f"ПРОВАЛОВ: {len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
