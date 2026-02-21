import os

# List of static export files to update
files = [
    r'_not-found/__next._index.txt',
    r'_not-found/__next._full.txt',
    r'_not-found/index.txt',
    r'places/__next._full.txt',
    r'places/__next._index.txt',
]

# Root directory
root = os.path.dirname(os.path.abspath(__file__))

for rel_path in files:
    abs_path = os.path.join(root, rel_path)
    if os.path.exists(abs_path):
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = content.replace('travelkutch.org', 'travelkutch.org')
        if new_content != content:
            with open(abs_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {rel_path}")
        else:
            print(f"No changes needed: {rel_path}")
    else:
        print(f"File not found: {rel_path}")
