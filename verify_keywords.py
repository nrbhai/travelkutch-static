#!/usr/bin/env python3
"""Verify keyword updates"""
import re
from pathlib import Path

files_to_check = [
    "index.html",
    "destinations/bhuj/index.html",
    "destinations/dhordo-white-rann/index.html",
    "crafts/ajrakh/index.html",
    "blog/rann-utsav-2025-guide/index.html"
]

for file_path in files_to_check:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.search(r'<meta name="keywords" content="([^"]*)"', content)
        if match:
            keywords = match.group(1)
            print(f"\n{file_path}:")
            print(f"  {keywords[:120]}...")
        else:
            print(f"\n{file_path}: NO KEYWORDS FOUND")
    except Exception as e:
        print(f"\n{file_path}: ERROR - {e}")
