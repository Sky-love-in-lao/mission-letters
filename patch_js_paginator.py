import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Update PAGE_HEIGHT_MM to 297 (full A4)
code = re.sub(r'const PAGE_HEIGHT_MM = 267;', r'const PAGE_HEIGHT_MM = 297;', code)

# Update the page creation style
target_style = """      p.style.height = PAGE_HEIGHT_MM + 'mm';
      p.style.columnCount = '2';
      p.style.columnGap = '7mm';
      p.style.columnFill = 'auto';
      p.style.overflow = 'hidden';
      p.style.position = 'relative';
      p.style.border = '12px solid transparent';
      p.style.borderImage = 'linear-gradient(to bottom, #CE1126 15%, #1e40af 15%, #1e40af 85%, #CE1126 85%) 1';
      p.style.padding = '0 4mm';
      p.style.boxSizing = 'border-box';"""

new_style = """      p.style.height = PAGE_HEIGHT_MM + 'mm';
      p.style.width = '210mm'; /* Full A4 width */
      p.style.columnCount = '2';
      p.style.columnGap = '7mm';
      p.style.columnFill = 'auto';
      p.style.overflow = 'hidden';
      p.style.position = 'relative';
      p.style.border = '14px solid transparent'; /* slightly thicker border */
      p.style.borderImage = 'linear-gradient(to bottom, #CE1126 15%, #1e40af 15%, #1e40af 85%, #CE1126 85%) 1';
      p.style.padding = '12mm 10mm'; /* Internal padding replacing the @page margin */
      p.style.boxSizing = 'border-box';"""

code = code.replace(target_style, new_style)

# Update container width from 180mm to 210mm (for accurate measuring)
code = re.sub(r"container\.style\.width = '180mm';", r"container.style.width = '210mm';", code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Patched JS paginator for edge-to-edge")
