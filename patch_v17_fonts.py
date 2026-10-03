import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Revert font sizes back to v15 levels to prevent 3-page spill
code = code.replace("pTag.style.fontSize = (12.5 * s) + 'pt';", "pTag.style.fontSize = (11 * s) + 'pt';")
code = code.replace("clone.querySelectorAll('.prayers__subtitle').forEach(el => el.style.fontSize = (14 * s) + 'pt');", "clone.querySelectorAll('.prayers__subtitle').forEach(el => el.style.fontSize = (13 * s) + 'pt');")
code = code.replace("clone.querySelectorAll('.prayers__text').forEach(el => el.style.fontSize = (13 * s) + 'pt');", "clone.querySelectorAll('.prayers__text').forEach(el => el.style.fontSize = (12 * s) + 'pt');")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V17 font revert")
