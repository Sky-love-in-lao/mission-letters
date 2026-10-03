import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = """  const photo = isPath
    ? `<img class="letter__hero-photo" src="${esc(src)}" alt="">`
    : `<a class="letter__hero-link" href="${esc(driveViewUrl(src))}" target="_blank" rel="noopener noreferrer" tabindex="-1" aria-hidden="true">
         <img class="letter__hero-photo" data-drive-id="${esc(src)}" alt="" referrerpolicy="no-referrer">
       </a>`;"""

new = """  const photo = isPath
    ? `<img class="letter__hero-photo" src="${esc(src)}" alt="">`
    : `<img class="letter__hero-photo" data-drive-id="${esc(src)}" alt="" referrerpolicy="no-referrer">`;"""

code = code.replace(target, new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V30: Removed hero image hyperlink wrapper")
