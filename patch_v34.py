import sys, re

# 1. Archive.js
file_archive = 'assets/js/views/archive.js'
with open(file_archive, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('<h1 class="archive__title">지난 선교편지</h1>', '<h1 class="archive__title">지난 ㅅ교편지</h1>')

target_link = "$('#archive-body', root).insertAdjacentHTML('beforeend',\n    '<p class=\"reader-foot\"><a href=\"#/settings\">선교사님이신가요? 편지 쓰러 가기</a></p>');"
code = code.replace(target_link, "")

with open(file_archive, 'w', encoding='utf-8') as f:
    f.write(code)

# 2. Render_v2.js defaults
file_render = 'assets/js/render_v2.js'
with open(file_render, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("'선교편지'", "'ㅅ교편지'")

with open(file_render, 'w', encoding='utf-8') as f:
    f.write(code)

# 3. app.js defaults
file_app = 'assets/js/app.js'
with open(file_app, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("선교편지", "ㅅ교편지")

with open(file_app, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V34: Masked '선교편지' to 'ㅅ교편지' and removed author link in archive")
