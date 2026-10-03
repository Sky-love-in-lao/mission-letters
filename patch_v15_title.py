import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = """           clone.querySelectorAll('.prayers__subtitle').forEach(el => el.style.fontSize = (13 * s) + 'pt');"""
new_code = """           clone.querySelectorAll('.prayers__title').forEach(el => el.style.fontSize = (15 * s) + 'pt');
           clone.querySelectorAll('.prayers__subtitle').forEach(el => el.style.fontSize = (13 * s) + 'pt');"""
code = code.replace(target, new_code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V15 title font size patch")
