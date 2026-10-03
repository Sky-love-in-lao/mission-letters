import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Change Prayer Title
# Current JS might have "두 손 모아 기도해 주세요" or "두손모아주세요요"
# We'll just replace the inner HTML of the h2.
code = re.sub(r'<h2 class="prayers__title">.*?</h2>', '<h2 class="prayers__title">ㄱ도해 주세요!</h2>', code)

# 2. Fix page width to 100% to remove white side-gaps (uneven border fix)
code = code.replace("p.style.width = '208mm';", "p.style.width = '100%';")

# 3. Increase base font sizes and prayer font sizes
# For normal text:
code = code.replace("pTag.style.fontSize = (10 * s) + 'pt';", "pTag.style.fontSize = (11 * s) + 'pt';")

# For prayers:
target_prayer_fonts = """           clone.querySelectorAll('.prayers__subtitle').forEach(el => el.style.fontSize = (11 * s) + 'pt');
           clone.querySelectorAll('.prayers__text').forEach(el => el.style.fontSize = (10 * s) + 'pt');"""
new_prayer_fonts = """           clone.querySelectorAll('.prayers__subtitle').forEach(el => el.style.fontSize = (13 * s) + 'pt');
           clone.querySelectorAll('.prayers__text').forEach(el => el.style.fontSize = (12 * s) + 'pt');"""
code = code.replace(target_prayer_fonts, new_prayer_fonts)

# 4. Decrease scale step from 0.04 to 0.02 to find a tighter fit (larger font)
code = code.replace("for (let s = 1.0; s >= 0.50; s -= 0.04) {", "for (let s = 1.0; s >= 0.50; s -= 0.02) {")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V15 patches: font sizes, 100% width, prayer title, scale step")
