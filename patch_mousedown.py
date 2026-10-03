import sys

file_path = 'assets/js/views/write_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = """  $$('.block__format button[data-action=bold]', wrap).forEach(button => {"""

replacement = """  $$('.block__format button', wrap).forEach(button => {
    button.onmousedown = e => e.preventDefault();
    button.ontouchstart = e => e.preventDefault();
  });

  $$('.block__format button[data-action=bold]', wrap).forEach(button => {"""

code = code.replace(target, replacement)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("patched mousedown")
