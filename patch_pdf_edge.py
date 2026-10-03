import sys, re

file_path = 'assets/css/app.css'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Replace @page margin
code = re.sub(r'@page\s*\{\s*size:\s*A4;\s*margin:\s*15mm;\s*\}', r'@page { size: A4 portrait; margin: 0; }', code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Patched @page margin")
