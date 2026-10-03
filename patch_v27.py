import sys

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Increase body text relative multiplier
code = code.replace("pTag.style.fontSize = (11 * s) + 'pt';", "pTag.style.fontSize = (13 * s) + 'pt';")

# 2. Shrink fixed photo sizes slightly to free up massive vertical space for the text
code = code.replace("img.style.maxHeight = '40mm';", "img.style.maxHeight = '35mm';")
code = code.replace("heroImg.style.maxHeight = '40mm';", "heroImg.style.maxHeight = '35mm';")

# 3. Compress Prayer Box margins/line-heights to reduce its overall height, but increase font multipliers
target_prayers = """           clone.querySelectorAll('.prayers__title').forEach(el => el.style.fontSize = (26 * s) + 'pt');
           clone.querySelectorAll('.prayers__subtitle').forEach(el => {
               el.style.fontSize = (20 * s) + 'pt';
               el.style.lineHeight = '1.4';
               el.style.display = 'block';
               el.style.marginBottom = '4px';
           });
           clone.querySelectorAll('.prayers__text').forEach(el => {
               el.style.fontSize = (18.5 * s) + 'pt';
               el.style.lineHeight = '1.6';
           });
           clone.querySelectorAll('.print-prayer-item').forEach(el => el.style.marginBottom = '30px');"""

new_prayers = """           clone.style.padding = '12px 16px'; // Shrink box padding
           clone.querySelectorAll('.prayers__title').forEach(el => {
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
           clone.querySelectorAll('.print-prayer-item').forEach(el => el.style.marginBottom = '12px'); // Drastically reduce margin!"""

code = code.replace(target_prayers, new_prayers)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V27 patches: boosted body text, shrank photos to free space, compressed prayer box margins, boosted prayer fonts")
