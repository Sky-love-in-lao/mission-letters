import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = "replace(/^[\d\s\.]*(라0스|물가|자녀|영육)/, '$1')"
new = "replace(/^[\d\s\.]*(라0스|라O스|라오스|물가|자녀|영육)/, '$1')"
code = code.replace(target, new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V36: Updated regex to support 라O스")
