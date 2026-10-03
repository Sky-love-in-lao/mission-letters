import sys, re

file_path = 'assets/js/views/write_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = "temp.className = 'page page--reader print-only';"
new_code = "temp.className = 'print-only';"
code = code.replace(target, new_code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Removed .page--reader class from temp to fix padding/margin spillover")
