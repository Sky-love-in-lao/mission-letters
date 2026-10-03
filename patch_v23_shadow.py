import sys

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = """      for (const page of finalPages) {
          page.style.boxShadow = '0 4px 12px rgba(0,0,0,0.5)';
          page.style.marginBottom = '20px';
      }"""
new = """      for (const page of finalPages) {
          // Combine drop shadow with the inner red borders!
          page.style.boxShadow = '0 4px 12px rgba(0,0,0,0.5), inset 0 14px 0 0 #CE1126, inset 0 -14px 0 0 #CE1126';
          page.style.marginBottom = '20px';
      }"""
code = code.replace(target, new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed shadow")
