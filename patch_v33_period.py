import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix heroHTML definition
target_def = "function heroHTML(src, size, body) {"
new_def = "function heroHTML(src, size, body, period) {"
code = code.replace(target_def, new_def)

# 2. Fix heroHTML call in letterHTML
target_call = "${heroSrc ? heroHTML(heroSrc, heroSize, body) : plainHeadHTML(body, period)}"
new_call = "${heroSrc ? heroHTML(heroSrc, heroSize, body, period) : plainHeadHTML(body, period)}"
code = code.replace(target_call, new_call)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V33: Fixed 'period is not defined' in heroHTML")
