import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = """      const clone = block.cloneNode(true);
      currentPage.appendChild(clone);
      
      if (currentPage.scrollWidth > currentPage.clientWidth + 2) {"""

new_code = """      const clone = block.cloneNode(true);
      if (clone.style) {
        clone.style.maxWidth = '100%';
        clone.style.boxSizing = 'border-box';
      }
      currentPage.appendChild(clone);
      
      // Use 15px tolerance for minor flex/grid overflow bugs in Chrome columns
      if (currentPage.scrollWidth > currentPage.clientWidth + 15) {"""

code = code.replace(target, new_code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Added max-width and tolerance to paginator")
