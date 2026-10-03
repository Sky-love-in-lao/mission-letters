import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Shrink images further to 32mm to guarantee massive text space
code = code.replace("img.style.maxHeight = '35mm';", "img.style.maxHeight = '32mm';")
code = code.replace("heroImg.style.maxHeight = '35mm';", "heroImg.style.maxHeight = '32mm';")

# 2. Boost body font multiplier to 14
code = code.replace("pTag.style.fontSize = (13 * s) + 'pt';", "pTag.style.fontSize = (14 * s) + 'pt';")

# 3. Compress Prayer Box even more tightly!
pattern = r"clone\.style\.padding = '12px 16px'; // Shrink box padding.*?clone\.style\.marginTop = '2mm';"
replacement = """clone.style.padding = '8px 12px'; // Extreme shrink box padding
           clone.querySelectorAll('.prayers__title, .print-prayer-title-wrapper').forEach(el => {
               el.style.fontSize = (30 * s) + 'pt';
               el.style.marginBottom = '6px';
           });
           clone.querySelectorAll('.prayers__subtitle').forEach(el => {
               el.style.fontSize = (22 * s) + 'pt';
               el.style.lineHeight = '1.1'; // Extremely tight line height
               el.style.display = 'block';
               el.style.marginBottom = '1px';
           });
           clone.querySelectorAll('.prayers__text').forEach(el => {
               el.style.fontSize = (20 * s) + 'pt';
               el.style.lineHeight = '1.25'; // Extremely tight line height
           });
           clone.querySelectorAll('.print-prayer-item').forEach(el => el.style.marginBottom = '6px'); // Extreme margin reduction!
           
           clone.style.marginTop = '2mm';"""

code = re.sub(pattern, replacement, code, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V28 extreme patches")
