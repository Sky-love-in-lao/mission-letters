import sys, re

file_path = 'assets/css/app.css'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Fix support__title
code = code.replace("font-size: clamp(16px, 4vw, 22px);", "font-size: 26px;")

# Fix print-prayer-box prayers__title (which overrides it at the bottom)
target_print_title = """.print-prayer-box .prayers__title {
  margin: 0;
  font-size: 18px;
  color: #000;
  font-weight: 800;
}"""
new_print_title = """.print-prayer-box .prayers__title {
  margin: 0;
  font-size: 26px;
  color: #000;
  font-weight: 800;
}"""
code = code.replace(target_print_title, new_print_title)

# Also ensure `.prayers__title` is large
target_prayer_title = """.prayers__title {
  font-family: var(--serif);
  font-size: 26px;""" # wait, I already replaced the clamp line, so it's 26px now!

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V37: Boosted section titles to 26px")
