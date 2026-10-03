import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = """    <figure class="letter__figure ${extraClass}">
      <a href="${href}" target="_blank" rel="noopener noreferrer">
        ${imgSrc}
      </a>
      <div class="letter__photo-fallback" hidden>${SHARE_HELP}</div>
      ${block.caption ? `<figcaption>${esc(block.caption)}</figcaption>` : ''}
    </figure>`;"""

new = """    <figure class="letter__figure ${extraClass}">
      ${imgSrc}
      <div class="letter__photo-fallback" hidden>${SHARE_HELP}</div>
      ${block.caption ? `<figcaption>${esc(block.caption)}</figcaption>` : ''}
    </figure>`;"""

code = code.replace(target, new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V30: Removed image hyperlink wrapper to disable photo enlargement")
