import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. FIX THE HORIZONTAL OVERFLOW BUG ON THE PRAYER BOX!
# The padding I added caused it to exceed 100% width, triggering the horizontal overflow check
# and generating a blank 3rd page, which crashed the scale 's' to 0.50!
target_padding = """clone.style.padding = '8px 12px'; // Extreme shrink box padding"""
new_padding = """clone.style.boxSizing = 'border-box'; // MUST BE BORDER-BOX OR IT OVERFLOWS HORIZONTALLY!
           clone.style.width = '100%';
           clone.style.maxWidth = '100%';
           clone.style.padding = '8px 12px';"""
code = code.replace(target_padding, new_padding)


# 2. To ensure MASSIVE text, let's keep the extreme layout from v28 but fix the text multipliers
# The user wants "글씨 크기를 더 크게해줘" (Make the font size larger)
# We will use 14 * s for body, and massive multipliers for prayers.
# Since the paginator will now actually stop at a large 's' (like 0.9 or 1.0), 
# 14 * 1.0 = 14pt! This is absolutely massive.
# Let's adjust prayers slightly so they fit cleanly.
pattern_prayers = r"clone\.querySelectorAll\('\.prayers__title, \.print-prayer-title-wrapper'\)\.forEach.*?clone\.style\.marginTop = '2mm';"
new_prayers = """clone.querySelectorAll('.prayers__title, .print-prayer-title-wrapper').forEach(el => {
               el.style.fontSize = (26 * s) + 'pt'; // Adjusted to fit perfectly
               el.style.marginBottom = '6px';
           });
           clone.querySelectorAll('.prayers__subtitle').forEach(el => {
               el.style.fontSize = (18 * s) + 'pt';
               el.style.lineHeight = '1.15'; 
               el.style.display = 'block';
               el.style.marginBottom = '1px';
           });
           clone.querySelectorAll('.prayers__text').forEach(el => {
               el.style.fontSize = (16 * s) + 'pt';
               el.style.lineHeight = '1.3'; 
           });
           clone.querySelectorAll('.print-prayer-item').forEach(el => el.style.marginBottom = '8px');
           
           clone.style.marginTop = '2mm';"""
code = re.sub(pattern_prayers, new_prayers, code, flags=re.DOTALL)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V29 patches: fixed horizontal overflow crashing scale, tuned fonts for massive body text")
