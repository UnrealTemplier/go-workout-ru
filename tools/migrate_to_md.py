"""
tools/migrate_to_md.py — разовый мигратор go-workout: JSON и Python-данные → Markdown в sources/ (трек Б, Б0–Б2).

Источники (старый генератор, builder/):
  * chapter{2..100}_data.json и section1..6.py (глава 1) — задачи;
  * build_all.py — hero и итоговый блок каждой главы, разделы глав (три формата), all_100_chapters
    (ключевые темы главы), learning_paths (7 траекторий);
  * builder/legacy_sources/N. Глава.md — краткие формулировки задач (правило U15).

Результат — дерево:
  sources/NNN. <Глава>/000. О главе.md
  sources/NNN. <Глава>/NN. <Раздел>/00. О разделе.md
  sources/NNN. <Глава>/NN. <Раздел>/KKK. <Задача>.md

Запуск из корня go-workout:
  python3 tools/migrate_to_md.py --names tools/short-names.tsv    # Б0: только список коротких имён
  python3 tools/migrate_to_md.py --out sources --report tools/migration-report.md
Проверка полноты — tools/verify_migration.py.
"""

import argparse
import ast
import collections
import glob
import html
import importlib.util
import json
import os
import re
import sys

LEGACY_SOURCES = os.path.join("builder", "legacy_sources")
TEXT_FIELDS = [
    ("task", None),
    ("theory", "Теория"),
    ("step_by_step", "Решение по шагам"),
    ("code_blocks", "Код решения"),
    ("under_the_hood", "Под капотом"),
    ("pitfalls", "Подводные камни"),
    ("bigtech_interview", "На собеседовании"),
    ("interview_qa", "На собеседовании"),
    ("best_practices", "Лучшие практики"),
    ("self_check", "Самопроверка"),
    ("test_cases", "Тест-кейсы"),
]
KNOWN_FIELDS = {"num", "title"} | {f for f, _ in TEXT_FIELDS}

# ---------------------------------------------------------------- загрузка данных


def load_tasks(repo):
    tasks = {}
    ch1 = []
    for i in range(1, 7):
        path = os.path.join(repo, "builder", f"section{i}.py")
        spec = importlib.util.spec_from_file_location(f"section{i}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        ch1 += mod.exercises
    tasks[1] = ch1
    for f in glob.glob(os.path.join(repo, "builder", "chapter*_data.json")):
        n = int(re.search(r"chapter(\d+)_data", f).group(1))
        with open(f, encoding="utf-8") as fp:
            tasks[n] = json.load(fp)
    return tasks


def _text(x):
    return html.unescape(" ".join(re.sub(r"<[^>]+>", "", x).split()))


def _strings(node):
    return [n.value for n in ast.walk(node) if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def load_meta(repo, tasks):
    """hero, итоговый блок и разделы каждой главы из функций build_chapterN_html."""
    with open(os.path.join(repo, "builder", "build_all.py"), encoding="utf-8") as fp:
        tree = ast.parse(fp.read())
    meta = {}
    for fn in tree.body:
        if not isinstance(fn, ast.FunctionDef):
            continue
        m = re.fullmatch(r"build_chapter(\d+)_html", fn.name)
        if not m:
            continue
        n = int(m.group(1))
        hero = next(s for s in _strings(fn) if 'class="hero-title"' in s)

        def grab(cls):
            return _text(re.search(r'class="%s"[^>]*>(.*?)</(?:div|h1|p)>' % cls, hero, re.S).group(1))
        footer = None
        for node in ast.walk(fn):
            if isinstance(node, (ast.Constant, ast.JoinedStr)):
                txt = node.value if isinstance(node, ast.Constant) else "".join(
                    v.value if isinstance(v, ast.Constant) else "{}" for v in node.values)
                if isinstance(txt, str) and "Поздравляем" in txt and "<h3" in txt:
                    h3 = re.search(r"<h3[^>]*>(.*?)</h3>", txt, re.S)
                    paras = [_text(x) for x in re.findall(r"<p[^>]*>(.*?)</p>", txt, re.S)]
                    footer = {"title": _text(h3.group(1)) if h3 else "", "paras": [p for p in paras if p]}
                    break
        sections = None
        for node in ast.walk(fn):
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.List) and node.value.elts \
                    and all(isinstance(e, ast.Tuple) for e in node.value.elts):
                sections = ast.literal_eval(node.value)
                break
        last = max(t["num"] for t in tasks[n])
        norm = []
        for i, s in enumerate(sections):
            if len(s) == 4:
                start, end, title, desc = s
            elif len(s) == 3:
                (start, end, title), desc = s, ""
            else:
                (start, title), desc = s, ""
                end = sections[i + 1][0] - 1 if i + 1 < len(sections) else last
            norm.append({"start": start, "end": end, "title": title, "desc": desc})
        meta[n] = {"hero_tag": grab("hero-(?:tag|badge)"), "hero_title": grab("hero-title"),
                   "hero_desc": grab("hero-desc"), "footer": footer, "sections": norm}
    return meta


def load_portal(repo):
    with open(os.path.join(repo, "builder", "build_all.py"), encoding="utf-8") as fp:
        tree = ast.parse(fp.read())
    topics, paths = {}, []
    for node in tree.body:
        if not (isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)):
            continue
        name = node.targets[0].id
        if name == "all_100_chapters":
            for e in node.value.elts:
                topics[ast.literal_eval(e.elts[0])] = ast.literal_eval(e.elts[5])
        elif name == "learning_paths":
            for d in node.value.elts:
                item = {}
                for k, v in zip(d.keys, d.values):
                    key = ast.literal_eval(k)
                    if key == "chapters" and isinstance(v, ast.Call):
                        item[key] = list(range(*[ast.literal_eval(x) for x in v.args[0].args]))
                    else:
                        item[key] = ast.literal_eval(v)
                paths.append(item)
    return topics, paths


def load_statements(repo, folder=LEGACY_SOURCES):
    """Краткие формулировки задач (старые sources/N. Глава.md): номер → текст, плюс вступление файла."""
    out = {}
    for f in glob.glob(os.path.join(repo, folder, "*.md")):
        base = os.path.basename(f)[:-3]
        m = re.match(r"^(\d+)\.\s*(.*)$", base)
        n = int(m.group(1))
        with open(f, encoding="utf-8") as fp:
            text = fp.read()
        intro, body = text.split("\n---\n", 1) if "\n---\n" in text else ("", text)
        items, cur, buf = {}, None, []
        for line in body.split("\n"):
            mm = re.match(r"^(\d+)\.\s+(.*)$", line)
            if mm and (cur is None or int(mm.group(1)) == cur + 1):
                if cur is not None:
                    items[cur] = "\n".join(buf).strip()
                cur, buf = int(mm.group(1)), [mm.group(2)]
            elif cur is not None:
                buf.append(line)
        if cur is not None:
            items[cur] = "\n".join(buf).strip()
        out[n] = {"title": m.group(2), "intro": intro.strip(), "items": items}
    return out


# ---------------------------------------------------------------- короткие имена (Б0)

NAME_MAX = 50
DANGLING = {"и", "в", "во", "на", "с", "со", "для", "по", "о", "об", "к", "ко", "из", "от", "без", "а", "но", "или",
            "через", "при", "до", "за", "над", "под", "про", "у", "vs", "and", "or", "the", "of", "in", "on", "to",
            "for", "with", "a", "an", "как", "что", "не", "между"}


def clean_name(title):
    t = title.replace(":", ".").replace("/", "_").replace("\\", "_")
    t = "".join(ch for ch in t if ch not in '*?"<>|' and ord(ch) >= 32)
    return re.sub(r"\s+", " ", t).strip()


def strip_section_title(title):
    t = re.sub(r"^\s*Раздел\s+\d+\s*[:.]\s*", "", title)
    return re.sub(r"\s*\((?:Упражнения|Задачи|Упр\.)\s*[\d–\-—, ]+\)\s*$", "", t)


def short_name(title, limit=NAME_MAX):
    raw = re.sub(r"\s+", " ", title).strip()
    if len(clean_name(raw)) > limit and ":" in raw:
        head = raw.split(":", 1)[0].strip()
        if 12 <= len(clean_name(head)) <= limit:
            raw = head
    t = clean_name(raw)
    if len(t) > limit:
        t2 = re.sub(r"\s*\([^()]*\)\s*$", "", t)
        if len(t2) >= 12:
            t = t2
    if len(t) > limit:
        cut = t[: limit + 1]
        best = max(cut.rfind(sep) for sep in (", ", " и ", " — ", "; "))
        if best >= 25:
            t = cut[:best]
        else:
            sp = cut.rfind(" ")
            t = cut[:sp] if sp >= 20 else t[:limit]
    while True:
        before = t
        t = t.rstrip(" .,;:-–—&+(")
        words = t.split(" ")
        if len(words) > 1 and words[-1].lower() in DANGLING:
            t = " ".join(words[:-1])
        if t.count("(") > t.count(")"):
            t = t[: t.rfind("(")].rstrip()
        if t == before:
            break
    return t or clean_name(title)[:limit]


def plan_names(tasks, meta, statements):
    """[(глава, раздел, задача или None, полное название, путь от sources/)]."""
    rows = []
    for n in sorted(tasks):
        ch_dir = f"{n:03d}. {short_name(statements[n]['title'])}"
        rows.append((n, None, None, statements[n]["title"], ch_dir))
        by_num = {t["num"]: t for t in tasks[n]}
        for si, sec in enumerate(meta[n]["sections"], 1):
            sec_dir = f"{ch_dir}/{si:02d}. {short_name(strip_section_title(sec['title']))}"
            rows.append((n, si, None, sec["title"], sec_dir))
            for k in range(sec["start"], sec["end"] + 1):
                t = by_num[k]
                rows.append((n, si, k, t["title"], f"{sec_dir}/{k:03d}. {short_name(t['title'])}.md"))
    return rows


# ---------------------------------------------------------------- Markdown

ESCAPABLE = set("\\`*_{}[]()>#+-.!")
CTRL = {"\r": "r", "\t": "t", "\x07": "a", "\x08": "b", "\x0c": "f", "\x0b": "v"}
SHELL_DOLLAR = re.compile(r"\$(?=\([a-z]|\{[A-Za-z_])")   # $(команда), ${VAR} — подстановки shell, не формулы
LATEXISH = re.compile(r"\\[A-Za-z]+|[\^_{}]|\\[,;!|%$&#]")
MATHISH = re.compile(r"^[\sA-Za-z0-9+\-*/=<>()|.,!'′≤≥≈×·∞%\[\]:]+$")


class Stats(collections.Counter):
    pass


def is_formula(content):
    if any(ch in CTRL for ch in content):
        return True                      # испорченная команда LaTeX (U25) — формула
    if not content.strip() or content != content.strip() and not LATEXISH.search(content):
        return False
    if LATEXISH.search(content):
        return True
    if re.search(r"[А-Яа-яЁё]", content):
        return False
    if re.search(r"[A-Za-z]{2,}/|/[A-Za-z]{2,}|[A-Za-z]:\S|:[A-Za-z$]", content):
        return False                                     # пути и списки PATH: $GOPATH/bin:$PATH
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9]{0,11}", content):
        return True                                      # переменная: $N$, $hLen$
    words = re.findall(r"\b[a-z]{3,}\b", content)
    if [w for w in words if w not in ("log", "sin", "cos", "max", "min", "mod", "exp", "len", "cap", "lim", "sum")]:
        return False                                     # английская проза между двумя $ (суммы в долларах)
    return bool(MATHISH.match(content)) and len(content) <= 40


CONTEXT = {"where": "", "u23": []}


def restore_ctrl(formula, log, stats):
    """U25: управляющий символ внутри формулы — испорченная команда LaTeX (CR вместо \\r и т. п.)."""
    out = []
    for i, ch in enumerate(formula):
        if ch in CTRL:
            out.append("\\" + CTRL[ch])
            stats["U25: восстановлено мест"] += 1
            log.append((CONTEXT["where"], repr(ch), "\\" + CTRL[ch] + formula[i + 1:i + 12]))
        else:
            out.append(ch)
    return "".join(out)


def escape_text(seg, stats):
    seg = re.sub(r"\\(?=[\\`*_{}\[\]()>#+\-.!])", lambda m: (stats.update(["\\ перед спецсимволом"]), "\\\\")[1], seg)
    seg = re.sub(r"&(?=#?[A-Za-z0-9]+;)", lambda m: (stats.update(["&сущность;"]), "&amp;")[1], seg)
    seg = re.sub(r"<(?=[A-Za-z/!?])", lambda m: (stats.update(["< тег"]), "&lt;")[1], seg)
    return seg


INLINE_CODE = re.compile(r"`[^`\n]*`")


def convert_line(line, stats, ctrl_log):
    """Строка текста вне ограды: код как есть, формулы — \\(…\\) / $$…$$, остальное экранировано."""
    out, pos = [], 0
    pieces = []
    for m in INLINE_CODE.finditer(line):
        pieces.append(("text", line[pos:m.start()]))
        pieces.append(("code", m.group(0)))
        pos = m.end()
    pieces.append(("text", line[pos:]))
    for kind, seg in pieces:
        if kind == "code":
            if "\x1b" in seg:
                # U25 в inline-коде: «\x1b» (ESC) в данных стал настоящим управляющим символом
                stats["U25: восстановлено мест"] += seg.count("\x1b")
                ctrl_log.append((CONTEXT["where"], "'\\x1b'", seg.replace("\x1b", "\\x1b")[:20]))
                seg = seg.replace("\x1b", "\\x1b")
            if len(seg) == 3 and seg[1] in CTRL:
                # U25 в inline-коде: `\t` в текстах главы 1 стал настоящим TAB
                stats["U25: восстановлено мест"] += 1
                ctrl_log.append((CONTEXT["where"], repr(seg[1]), "`\\" + CTRL[seg[1]] + "`"))
                seg = "`\\" + CTRL[seg[1]] + "`"
            out.append(seg)
            continue
        out.append(convert_math(seg, stats, ctrl_log))
    res = "".join(out)
    stripped = res.lstrip()
    indent = res[: len(res) - len(stripped)]
    if stripped.startswith("#") and not re.match(r"#{3,4} ", stripped):
        res = indent + "\\" + stripped
        stats["строка на # экранирована"] += 1
    elif re.match(r"\+\s", stripped):
        res = indent + "\\" + stripped
        stats["строка на + экранирована"] += 1
    return res


def convert_math(seg, stats, ctrl_log):
    out = []
    i = 0
    parts = re.split(r"(\$\$.*?\$\$)", seg)
    for part in parts:
        if part.startswith("$$") and part.endswith("$$") and len(part) > 4:
            out.append(restore_ctrl(part, ctrl_log, stats))
            stats["формула $$…$$"] += 1
            continue
        marks = [m.start() for m in re.finditer(r"(?<!\\)\$", part)
                 if not SHELL_DOLLAR.match(part, m.start())]
        tail = ""
        if len(marks) % 2 and part[marks[-1] + 1:marks[-1] + 2] in CTRL and part[marks[-1] + 1:marks[-1] + 2]:
            # U25: «$\rightarrow» без закрывающего $ — испорченная команда; формула закрывается после неё
            a = marks.pop()
            cmd = re.match(r".[A-Za-z]*", part[a + 1:]).group(0)
            stats["U25: формула без закрывающего $ закрыта"] += 1
            tail = "\\(" + restore_ctrl(cmd, ctrl_log, stats) + "\\)" + escape_text(part[a + 1 + len(cmd):], stats)
            part = part[:a]
        res, last = [], 0
        k = 0
        while k + 1 < len(marks):
            a, b = marks[k], marks[k + 1]
            content = part[a + 1:b]
            if is_formula(content):
                res.append(escape_text(part[last:a], stats))
                res.append("\\(" + restore_ctrl(content, ctrl_log, stats) + "\\)")
                stats["формула $…$ → \\(…\\)"] += 1
                last = b + 1
                k += 2
            else:
                stats["$…$ не формула (остался текстом)"] += 1
                k += 1
        res.append(escape_text(part[last:], stats))
        out.append("".join(res) + tail)
    return "".join(out)


def field_text(v):
    if isinstance(v, list):
        v = "\n".join(str(x) for x in v)
    return v.strip()


LF_COMMAND = re.compile(r"\n(?=(?:e|eq|abla|u|ot|ewline)\b)")


def restore_lf(text, stats, log):
    """U25: перевод строки внутри формулы перед хвостом команды — испорченное \\n (\\ne, \\neq, \\nabla…)."""
    def fix(m):
        span = m.group(0)
        new = LF_COMMAND.sub(lambda mm: (stats.update(["U25: восстановлено мест"]),
                                         log.append((CONTEXT["where"], "'\\n'", "\\n" + span[mm.end():mm.end() + 10])),
                                         "\\n")[2], span)
        return new
    parts = re.split(r"(```.*?```)", text, flags=re.S)
    return "".join(p if p.startswith("```") else re.sub(r"\$\$.*?\$\$|\$[^$]*?\$", fix, p, flags=re.S)
                   for p in parts)


def close_fence(text, stats):
    """Ограда, оставшаяся открытой в исходных данных: старый сайт показывал пустой блок кода — закрываем."""
    if sum(1 for l in text.split("\n") if l.strip().startswith("```")) % 2:
        stats["U23: незакрытая ограда в данных закрыта"] += 1
        last = [l.strip() for l in text.split("\n") if l.strip().startswith("```")][-1]
        CONTEXT["u23"].append((CONTEXT["where"], last))
        return text + "\n```"
    return text


def restore_crlf_code(text, stats, log):
    """U25: «\\r\\n» внутри inline-кода стал настоящими CR LF (`NATS/1.0\\r\\n…`) — возвращаем буквальный текст."""
    def fix(m):
        stats["U25: \\r\\n в inline-коде восстановлено"] += 1
        log.append((CONTEXT["where"], "'\\r\\n'", m.group(0)[:20].replace("\r\n", "\\r\\n")))
        return m.group(0).replace("\r\n", "\\r\\n")
    return re.sub(r"`[^`]*\r\n[^`]*`", fix, text)


def field_md(v, stats, ctrl_log):
    text = close_fence(restore_lf(restore_crlf_code(field_text(v), stats, ctrl_log), stats, ctrl_log), stats)
    lines = text.split("\n")
    out, fence, fence_mark = [], False, ""
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if s.startswith("```"):
            if not fence:
                fence, fence_mark = True, s[:3]
            else:
                fence = False
            out.append(line)
        elif fence:
            out.append(line)
        else:
            # многострочная формула $$ … $$ без пустых строк внутри
            if s == "$$" or (s.startswith("$$") and s.count("$$") == 1):
                block = [line]
                j = i + 1
                while j < len(lines) and "$$" not in lines[j]:
                    if lines[j].strip():
                        block.append(lines[j])
                    j += 1
                if j < len(lines):
                    block.append(lines[j])
                    out.append(restore_ctrl("\n".join(block), ctrl_log, stats))
                    stats["формула $$ многострочная"] += 1
                    i = j + 1
                    continue
            if re.fullmatch(r"(-{3,}|\*{3,}|_{3,}|={3,})", s) and out and out[-1].strip():
                out.append("")
                stats["пустая строка перед ---"] += 1
            out.append(convert_line(line, stats, ctrl_log))
        i += 1
    return "\n".join(out)


def norm_compare(t):
    t = re.sub(r"[`*]", "", t)
    return re.sub(r"\s+", " ", t).strip().rstrip(".").lower()


def fence_for(code):
    longest = max((len(m) for m in re.findall(r"`+", code)), default=0)
    return "`" * max(3, longest + 1)


def code_md(cb, stats, ctrl_log):
    code = cb["code"].strip("\n")
    fence = fence_for(code)
    name = cb.get("filename") or ""
    tick = "``" if "`" in name else "`"
    parts = []
    if name:
        parts.append(f"**{tick}{name}{tick}**" if tick == "`" else f"**{tick} {name} {tick}**")
        parts.append("")
    parts.append(f"{fence}{cb.get('lang') or 'go'}")
    parts.append(code)
    parts.append(fence)
    if cb.get("note"):
        parts.append("")
        parts.append("ℹ️ " + convert_line(cb["note"].strip(), stats, ctrl_log))
    stats["блоков кода"] += 1
    return "\n".join(parts)


def test_cases_md(cases):
    out = []
    for c in cases:
        out.append(f"- **{c.get('name', '')}**")
        for key, label in (("input", "Вход"), ("expected", "Ожидается")):
            if key in c:
                val = c[key] if isinstance(c[key], str) else json.dumps(c[key], ensure_ascii=False)
                if "\n" in val:
                    fence = fence_for(val)
                    out.append(f"  - {label}:")
                    out.append("")
                    out.append(f"    {fence}text")
                    out.extend("    " + l for l in val.split("\n"))
                    out.append(f"    {fence}")
                else:
                    tick = "``" if "`" in val else "`"
                    pad = " " if tick == "``" else ""
                    out.append(f"  - {label}: {tick}{pad}{val}{pad}{tick}")
        extra = {k: v for k, v in c.items() if k not in ("name", "input", "expected")}
        if extra:
            out.append(f"  - Прочее: `{json.dumps(extra, ensure_ascii=False)}`")
    return "\n".join(out)


def task_md(t, statement, stats, ctrl_log):
    unknown = set(t) - KNOWN_FIELDS
    if unknown:
        raise ValueError(f"неизвестные поля {unknown} в задаче {t['num']}")
    out = [f"# {t['title']}", "", "## Условие", ""]
    task_text = field_text(t["task"])
    if statement is not None:
        statement = close_fence(statement, stats)
    if statement is not None and norm_compare(task_text) == norm_compare(statement):
        out.append(statement)
        stats["U15: условие совпало, взят текст sources"] += 1
    else:
        out.append(field_md(t["task"], stats, ctrl_log))
        if statement is not None:
            out += ["", "### Исходная формулировка", "", statement]
            stats["U15: добавлена исходная формулировка"] += 1
    for f, title in TEXT_FIELDS[1:]:
        v = t.get(f)
        if not v:
            continue
        out += ["", f"## {title}", ""]
        if f == "code_blocks":
            out.append("\n\n".join(code_md(cb, stats, ctrl_log) for cb in v))
        elif f == "test_cases":
            out.append(test_cases_md(v))
        elif f == "best_practices" and isinstance(v, list):
            out.append("\n".join("- " + convert_line(str(x).strip(), stats, ctrl_log) for x in v))
        else:
            out.append(field_md(v, stats, ctrl_log))
    return "\n".join(out).rstrip() + "\n"


def chapter_md(n, meta, topics, statements, stats, ctrl_log):
    m = meta[n]
    out = [f"# {m['hero_title']}", "", f"*{convert_line(m['hero_tag'], stats, ctrl_log)}*", "",
           convert_line(m["hero_desc"], stats, ctrl_log)]
    if topics.get(n):
        out += ["", "**Ключевые темы:** " + convert_line(topics[n], stats, ctrl_log)]
    intro = statements[n]["intro"]
    if intro:
        lines = intro.split("\n")
        if lines and lines[0].startswith("# "):
            head = lines[0][2:].strip()
            lines = lines[1:]
            if head != m["hero_title"]:
                lines = [f"**{head}**", ""] + lines
        body = "\n".join(lines).strip()
        if body:
            out += ["", "## Об упражнениях главы", "", body]
    if m["footer"]:
        out += ["", "## Итог главы", ""]
        if m["footer"]["title"]:
            out += [f"**{convert_line(m['footer']['title'], stats, ctrl_log)}**", ""]
        out += [convert_line(p, stats, ctrl_log) + "\n" for p in m["footer"]["paras"]]
    return "\n".join(out).rstrip() + "\n"


def section_md(sec, stats, ctrl_log):
    out = [f"# {sec['title']}"]
    if sec["desc"]:
        out += ["", convert_line(sec["desc"], stats, ctrl_log)]
    return "\n".join(out) + "\n"


def migrate(repo, out_dir):
    tasks = load_tasks(repo)
    meta = load_meta(repo, tasks)
    topics, paths = load_portal(repo)
    statements = load_statements(repo)
    rows = plan_names(tasks, meta, statements)
    stats, ctrl_log = Stats(), []
    CONTEXT["u23"] = []
    written = 0
    by_num = {n: {t["num"]: t for t in tasks[n]} for n in tasks}
    for n, si, k, full, rel in rows:
        CONTEXT["where"] = rel
        path = os.path.join(out_dir, rel)
        if si is None:
            os.makedirs(path, exist_ok=True)
            text = chapter_md(n, meta, topics, statements, stats, ctrl_log)
            path = os.path.join(path, "000. О главе.md")
        elif k is None:
            os.makedirs(path, exist_ok=True)
            text = section_md(meta[n]["sections"][si - 1], stats, ctrl_log)
            path = os.path.join(path, "00. О разделе.md")
        else:
            text = task_md(by_num[n][k], statements[n]["items"].get(k), stats, ctrl_log)
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(text)
        written += 1
    return {"tasks": tasks, "meta": meta, "topics": topics, "paths": paths, "statements": statements,
            "rows": rows, "stats": stats, "ctrl": ctrl_log, "u23": list(CONTEXT["u23"]), "written": written}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Мигратор go-workout в Markdown")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--names", help="записать только список коротких имён (TSV) и выйти")
    ap.add_argument("--out", help="каталог для дерева Markdown (обычно sources)")
    ap.add_argument("--report", help="отчёт мигратора (Markdown)")
    args = ap.parse_args(argv)
    if args.names:
        tasks = load_tasks(args.repo)
        meta = load_meta(args.repo, tasks)
        statements = load_statements(args.repo)
        rows = plan_names(tasks, meta, statements)
        with open(args.names, "w", encoding="utf-8") as fp:
            fp.write("глава\tраздел\tзадача\tполное название\tпуть от sources/\n")
            for n, si, k, full, rel in rows:
                fp.write(f"{n}\t{si or ''}\t{k or ''}\t{full}\t{rel}\n")
        print(f"{args.names}: {len(rows)} строк")
        return 0
    if not args.out:
        ap.error("нужен --out или --names")
    res = migrate(args.repo, args.out)
    print(f"записано файлов: {res['written']}")
    for k, v in sorted(res["stats"].items()):
        print(f"  {k}: {v}")
    if args.report:
        write_report(args.report, res)
    return 0


def write_report(path, res):
    s = res["stats"]
    lines = ["# Отчёт мигратора go-workout", "",
             "Сгенерирован `python3 tools/migrate_to_md.py`; вручную не править.", "",
             f"* Глав: {len(res['tasks'])}, разделов: {sum(len(m['sections']) for m in res['meta'].values())}, "
             f"задач: {sum(len(v) for v in res['tasks'].values())}, файлов: {res['written']}.", "",
             "## Счётчики преобразований (анализ § 7.5)", "", "| Класс | Сколько |", "|---|--:|"]
    for k, v in sorted(s.items()):
        lines.append(f"| {k} | {v} |")
    lines += ["", f"## U25: восстановленные команды LaTeX ({len(res['ctrl'])})", "",
              "| Файл (`sources/`) | Символ | Стало |", "|---|---|---|"]
    for where, ch, after in res["ctrl"]:
        lines.append(f"| `{where}` | {ch} | `` {after} `` |")
    lines += ["", f"## U23: закрытые ограды ({len(res['u23'])})", "",
              "Ограда открыта в исходных данных и не закрыта; мигратор добавил закрывающую строку ```` ``` ```` в конец текста.", "",
              "| Файл (`sources/`) | Открывающая строка |", "|---|---|"]
    for where, fence in res["u23"]:
        lines.append(f"| `{where}` | `` {fence} `` |")
    with open(path, "w", encoding="utf-8") as fp:
        fp.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    sys.exit(main())
