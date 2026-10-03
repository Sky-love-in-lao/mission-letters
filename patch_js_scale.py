import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = """  for (const page of finalPages) {
    page.style.breakAfter = 'page';"""

new_code = """  for (const page of finalPages) {
    page.style.setProperty('--print-scale', bestScale.toString());
    page.style.breakAfter = 'page';"""

code = code.replace(target, new_code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied print-scale directly to pages")
