import sys, re

file_js = 'assets/js/render_v2.js'
with open(file_js, 'r', encoding='utf-8') as f:
    code = f.read()

target = '<h2 class="support__title">💌 사역에 동참하기</h2>'
new_html = '<h2 class="support__title">💌 사역에 동참하기</h2>\n      <p class="support__alert" style="color: #dc2626; font-weight: bold; font-size: 15px; margin: 0 0 16px; word-break: keep-all; line-height: 1.5;">첫 송금시 ㅅ교국(02-3459-1031~4)으로 전화 후 박OO/김OO ㅅ교사 후원임을 꼭 알려주세요!</p>'

if target in code:
    code = code.replace(target, new_html)
else:
    print("Could not find target html in render_v2.js")

with open(file_js, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V41: Added wire transfer instructions to support section")
