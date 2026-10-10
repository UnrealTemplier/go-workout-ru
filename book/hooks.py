"""
book/hooks.py — хуки go-workout для html-textbook-engine (engine/hooks.py).

extra_audit_checks: gofmt -e по всем блокам Go в собранном dist/ (анализ § 7.6, проверка 5).
Проверяются блоки с объявлением package: go.mod и go.work в данных тоже помечены языком go.
Если gofmt не найден, проверка пропускается с предупреждением (как рантайм-разбор без Firefox).
"""

import html
import os
import re
import shutil
import subprocess
import tempfile

GO_BLOCK = re.compile(r'<pre class="language-go"><code class="language-go">(.*?)</code></pre>', re.S)
PACKAGE = re.compile(r"^package \w+", re.M)


def extra_audit_checks(dist_dir):
    gofmt = shutil.which("gofmt")
    if not gofmt:
        print("⚠️  gofmt не найден: проверка блоков Go пропущена")
        return []
    blocks = []
    for root, _, files in os.walk(os.path.join(dist_dir, "docs")):
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as fp:
                for m in GO_BLOCK.finditer(fp.read()):
                    code = html.unescape(m.group(1))
                    if PACKAGE.search(code):
                        blocks.append((os.path.relpath(path, dist_dir), code))
    errors = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, (_, code) in enumerate(blocks):
            with open(os.path.join(tmp, f"b{i}.go"), "w", encoding="utf-8") as fp:
                fp.write(code + "\n")
        res = subprocess.run([gofmt, "-e", "-l", tmp], capture_output=True, text=True)
        seen = set()
        for line in res.stderr.splitlines():
            m = re.match(r".*/b(\d+)\.go:(\d+:\d+): (.*)", line)
            if m and int(m.group(1)) not in seen:
                seen.add(int(m.group(1)))
                errors.append(f"gofmt -e: {blocks[int(m.group(1))][0]}: {m.group(2)}: {m.group(3)}")
    print(f"      Блоков Go проверено gofmt -e: {len(blocks)}")
    return errors
