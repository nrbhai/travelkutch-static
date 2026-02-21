#!/usr/bin/env python3
"""
fix_domain_seo.py
-----------------
Replaces ALL occurrences of 'travelkutch.org' with 'travelkutch.org'
across every file in the website project (HTML, txt, json, css, js, etc.)
Skips binary files, .git directory, .venv, and image/video assets.
"""

import os
import sys

# ── configuration ────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
OLD  = 'travelkutch.org'
NEW  = 'travelkutch.org'

# Extensions to process  (add more as needed)
TEXT_EXTENSIONS = {
    '.html', '.htm', '.txt', '.json', '.xml', '.js', '.css',
    '.md', '.py', '.csv', '.svg', '.ts', '.tsx', '.jsx',
}

# Directories to skip entirely
SKIP_DIRS = {'.git', '.venv', '__pycache__', 'node_modules'}

# ── helpers ──────────────────────────────────────────────────────────────────
def is_text_file(path: str) -> bool:
    """Return True if we should process this file."""
    _, ext = os.path.splitext(path)
    return ext.lower() in TEXT_EXTENSIONS

def process_file(path: str) -> bool:
    """Replace OLD→NEW in file. Return True if file was changed."""
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f'  [SKIP] Cannot read {path}: {e}')
        return False

    if OLD not in content:
        return False

    new_content = content.replace(OLD, NEW)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except Exception as e:
        print(f'  [ERROR] Cannot write {path}: {e}')
        return False

    return True

# ── main ─────────────────────────────────────────────────────────────────────
def main():
    changed_files = []
    scanned = 0

    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Skip unwanted directories
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if not is_text_file(filepath):
                continue
            scanned += 1
            if process_file(filepath):
                rel = os.path.relpath(filepath, ROOT)
                changed_files.append(rel)
                print(f'  [UPDATED] {rel}')

    print()
    print('=' * 60)
    print(f'Scanned : {scanned} text files')
    print(f'Updated : {len(changed_files)} files')
    print('=' * 60)

    if changed_files:
        print('\nFiles changed:')
        for f in changed_files:
            print(f'  {f}')
    else:
        print('\nNo files contained the old domain — nothing to change.')

if __name__ == '__main__':
    main()
