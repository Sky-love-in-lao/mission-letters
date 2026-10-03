import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = "if (currentPage.scrollWidth > currentPage.clientWidth + 5 || currentPage.scrollHeight > currentPage.clientHeight + 5) {"
new_code = "if (currentPage.scrollWidth > currentPage.clientWidth + 2) {"

code = code.replace(target, new_code)

# Let's also ensure images inside .letter__row don't break column-count by setting them to inline-block if needed.
# Actually, the false positive was due to scrollHeight. Removing scrollHeight check should fix it.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Removed scrollHeight check to prevent false page breaks")
