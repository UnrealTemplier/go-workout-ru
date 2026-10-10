import os
import glob
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SOURCES_DIR = os.path.join(REPO_ROOT, "builder", "legacy_sources")  # краткие формулировки задач старого генератора

TRANSLIT_MAP = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
}

def slugify_title(num, title):
    text = title.lower()
    res = []
    for ch in text:
        if ch in TRANSLIT_MAP:
            res.append(TRANSLIT_MAP[ch])
        elif ch.isalnum():
            res.append(ch)
        else:
            res.append('-')
    slug = ''.join(res)
    slug = re.sub(r'-+', '-', slug).strip('-')
    return f"{num:03d}-{slug}.html"

def get_all_chapters():
    files = glob.glob(os.path.join(SOURCES_DIR, "*.md"))
    chapters = []
    for f in files:
        base = os.path.basename(f)
        name_without_ext = os.path.splitext(base)[0]
        m = re.match(r'^(\d+)\.\s*(.*)$', name_without_ext)
        if not m:
            continue
        num = int(m.group(1))
        title = m.group(2)
        html_filename = slugify_title(num, title)
            
        chapters.append({
            'num': num,
            'title': title,
            'filename': base,
            'html_filename': html_filename,
            'is_current': (num == 1),
            'status': 'Готово (91/91)' if num == 1 else 'В разработке'
        })
    chapters.sort(key=lambda c: c['num'])
    return chapters

def get_chapter_url_map():
    chapters = get_all_chapters()
    return {c['num']: c['html_filename'] for c in chapters}

if __name__ == '__main__':
    ch = get_all_chapters()
    print(f"Loaded {len(ch)} chapters.")
    print("First chapter:", ch[0])
    print("Last chapter:", ch[-1])
