import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Completely wipe the messy prayer font lines and replace them with the clean ones
pattern = r"clone\.querySelectorAll\('\.prayers__title, \.print-prayer-title-wrapper'\).*?el\.style\.marginBottom = '30px'\);"

replacement = """clone.style.padding = '12px 16px'; // Shrink box padding
           clone.querySelectorAll('.prayers__title, .print-prayer-title-wrapper').forEach(el => {
               el.style.fontSize = (28 * s) + 'pt';
               el.style.marginBottom = '10px';
           });
           clone.querySelectorAll('.prayers__subtitle').forEach(el => {
               el.style.fontSize = (21 * s) + 'pt';
               el.style.lineHeight = '1.25'; // Tight line height to save box height!
               el.style.display = 'block';
               el.style.marginBottom = '2px';
           });
           clone.querySelectorAll('.prayers__text').forEach(el => {
               el.style.fontSize = (19.5 * s) + 'pt';
               el.style.lineHeight = '1.35'; // Tight line height!
           });
           clone.querySelectorAll('.print-prayer-item').forEach(el => el.style.marginBottom = '12px');"""

# Wait, `re.sub` with re.DOTALL
code = re.sub(pattern, replacement, code, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V27 prayer box fix")
