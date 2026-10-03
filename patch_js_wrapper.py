import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = """            currentBlocks.push(...Array.from(textBlock.children));"""

new_code = """            for (const p of Array.from(textBlock.children)) {
              const wrapper = document.createElement('div');
              wrapper.className = 'letter__text';
              wrapper.appendChild(p.cloneNode(true));
              currentBlocks.push(wrapper);
            }"""

code = code.replace(target, new_code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Wrapped flattened paragraphs in letter__text")
