#!/usr/bin/env python3
"""
sync.py — Sincroniza los textos del Notebook al _posts/ del Jekyll.

Lee archivos numerados ("01 Título.md", "02 Otro.md", ...) desde
NOTEBOOK_DIR, los ordena por número, transforma `{centered}` a kramdown
IAL (`{:.centered}`), y escribe los _posts/ correspondientes con front
matter listo para Jekyll.

Convenciones:
  - El nombre del archivo determina título y orden:
        "01 Dhul-Qarnayn.md"  →  título "Dhul-Qarnayn", número 01
  - El número decide la posición en la home: 01 arriba (más reciente
    en la fecha sintética), N abajo.
  - Líneas que empiezan con `{centered}` se centran como invocaciones.
  - Cada corrida BORRA y regenera _posts/. Edita siempre en NOTEBOOK_DIR.
"""

import re
import sys
import unicodedata
from datetime import datetime, timedelta
from pathlib import Path

NOTEBOOK_DIR = Path("/home/dajjal/Notebook/Templo de Venus/Page")
POSTS_DIR = Path(__file__).resolve().parent.parent / "_posts"
TZ_OFFSET = "-0600"

FILENAME_PATTERN = re.compile(r"^(\d+)\s+(.+)\.md$")


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def transform_centered(body: str) -> str:
    out = []
    for line in body.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("{centered}"):
            content = stripped[len("{centered}"):].lstrip()
            if out and out[-1].strip() != "":
                out.append("")
            out.append(content)
            out.append("{:.centered}")
            out.append("")
        else:
            out.append(line)

    cleaned = []
    blank_streak = 0
    for line in out:
        if line.strip() == "":
            blank_streak += 1
            if blank_streak <= 1:
                cleaned.append(line)
        else:
            blank_streak = 0
            cleaned.append(line)
    return "\n".join(cleaned).strip() + "\n"


def strip_existing_front_matter(raw: str) -> str:
    if not raw.startswith("---\n"):
        return raw
    closing = raw.find("\n---", 4)
    if closing == -1:
        return raw
    return raw[closing + 4:].lstrip("\n")


def parse_filename(name: str):
    m = FILENAME_PATTERN.match(name)
    if not m:
        return None
    return int(m.group(1)), m.group(2).strip()


def main():
    if not NOTEBOOK_DIR.is_dir():
        sys.exit(f"No existe el notebook: {NOTEBOOK_DIR}")
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    entries = []
    skipped = []
    for path in sorted(NOTEBOOK_DIR.iterdir()):
        if not path.is_file() or path.suffix.lower() != ".md":
            continue
        parsed = parse_filename(path.name)
        if parsed is None:
            skipped.append(path.name)
            continue
        number, title = parsed
        entries.append((number, title, path))

    if skipped:
        print("Ignorados (no respetan el patrón 'NN título.md'):")
        for name in skipped:
            print(f"  · {name}")
        print()

    if not entries:
        print("No hay archivos numerados en", NOTEBOOK_DIR)
        return

    entries.sort(key=lambda e: e[0])

    for old in POSTS_DIR.glob("*.md"):
        old.unlink()

    base = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    print(f"Sincronizando {len(entries)} textos → {POSTS_DIR}\n")

    for index, (number, title, src) in enumerate(entries):
        post_dt = base - timedelta(minutes=index)
        date_str = post_dt.strftime("%Y-%m-%d %H:%M:%S") + " " + TZ_OFFSET
        ymd = post_dt.strftime("%Y-%m-%d")

        raw = src.read_text(encoding="utf-8")
        raw = strip_existing_front_matter(raw)
        body = transform_centered(raw)

        slug = slugify(title)
        target = POSTS_DIR / f"{ymd}-{slug}.md"

        front = (
            "---\n"
            f"title: {title}\n"
            f"date: {date_str}\n"
            "---\n\n"
        )
        target.write_text(front + body, encoding="utf-8")
        print(f"  {number:02d}  {title}")
        print(f"      → {target.name}")

    print(f"\nListo. Ahora: git add . && git commit -m '...' && git push")


if __name__ == "__main__":
    main()
