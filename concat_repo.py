#!/usr/bin/env python3
"""
Concatenate all key source, proof, and config files for the Black_whole_article project.

Включает только важные для воспроизводимости и проверки файлы:
- article_blackhole_inevitable_en.md
- LeanBh/*.lean
- ai_black_hole_time_to_threshold.py, get_phi_years.py
- logic-graph.yml
- plugins/**/*.py
- README.md
- setup.py, lakefile.toml, lake-manifest.json

Исключает всё лишнее (egg-info, .lake, .git, build, dist, node_modules, кэш, картинки и т.д.)

Usage:
    $ python concat_repo.py
"""
import os
from pathlib import Path

INCLUDE_PATHS = [
    "article_blackhole_inevitable_en.md",
    "README.md",
    "logic-graph.yml",
    "setup.py",
    "lakefile.toml",
    "lake-manifest.json",
    "ai_black_hole_time_to_threshold.py",
    "get_phi_years.py",
]

INCLUDE_DIRS = [
    ("LeanBh", ".lean"),
    ("plugins", ".py"),
]

EXCLUDE_DIRS = {".git", ".lake", "__pycache__", ".venv", "venv", "build", "dist", "node_modules", "bh_veritas_plugins.egg-info", "src", "viz"}

OUT_FILE = "repo_concat.txt"
MAX_BYTES = 200_000
MAX_LINES = 400

def iter_files():
    # Файлы по явному списку
    for fname in INCLUDE_PATHS:
        path = Path(fname)
        if path.exists() and path.is_file():
            yield path
    # Файлы по директориям и расширениям
    for dname, ext in INCLUDE_DIRS:
        d = Path(dname)
        if not d.exists():
            continue
        for root, dirs, files in os.walk(d):
            # Пропускаем вложенные исключённые папки
            dirs[:] = [dd for dd in dirs if dd not in EXCLUDE_DIRS and not dd.startswith('.')]
            for f in files:
                if not f.endswith(ext):
                    continue
                p = Path(root) / f
                if p.stat().st_size > MAX_BYTES:
                    continue
                yield p

def write_concat():
    with open(OUT_FILE, "w", encoding="utf-8", errors="ignore") as fout:
        fout.write("# Black_whole_article: Key Source, Proof, and Config Files\n\n")
        for path in iter_files():
            try:
                rel = path.relative_to(Path.cwd())
            except ValueError:
                rel = path.name
            header = f"===== {rel} ====="
            fout.write(header + "\n" + ("-" * len(header)) + "\n")
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
            if MAX_LINES and len(lines) > MAX_LINES:
                lines = lines[:MAX_LINES] + [f"... (truncated {len(lines)-MAX_LINES} lines) ..."]
            fout.write("\n".join(lines) + "\n\n")
    print(f"Wrote {OUT_FILE} with {sum(1 for _ in iter_files())} files.")

if __name__ == "__main__":
    write_concat() 