import sys, re

# 1. Update letter.js
file_js = 'assets/js/views/letter.js'
with open(file_js, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('<h1 class="lock__title">ㅅ교편지</h1>', '<h1 class="lock__title">라O스 박OO, 김OO ㅅ교편지</h1>')

with open(file_js, 'w', encoding='utf-8') as f:
    f.write(code)

# 2. Update app.css
file_css = 'assets/css/app.css'
with open(file_css, 'r', encoding='utf-8') as f:
    code = f.read()

target_desc = ".lock__desc { font-size: 15px; color: var(--ink-soft); margin: 0 0 28px; line-height: 1.75; }"
new_desc = ".lock__desc { font-size: 18px; color: #2563eb; font-weight: 600; margin: 0 0 28px; line-height: 1.75; }"

code = code.replace(target_desc, new_desc)

with open(file_css, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V39: Updated lock title and description styling")
