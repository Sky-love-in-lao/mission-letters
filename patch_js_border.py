import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = """      p.style.height = PAGE_HEIGHT_MM + 'mm';
      p.style.width = '210mm'; /* Full A4 width */
      p.style.columnCount = '2';
      p.style.columnGap = '7mm';
      p.style.columnFill = 'auto';
      p.style.overflow = 'hidden';
      p.style.position = 'relative';
      p.style.border = '14px solid transparent'; /* slightly thicker border */
      p.style.borderImage = 'linear-gradient(to bottom, #CE1126 15%, #1e40af 15%, #1e40af 85%, #CE1126 85%) 1';
      p.style.padding = '8mm 6mm'; /* Internal padding replacing the @page margin */
      p.style.boxSizing = 'border-box';"""

new_code = """      p.style.height = PAGE_HEIGHT_MM + 'mm';
      p.style.width = '210mm';
      p.style.position = 'relative';
      p.style.background = 'linear-gradient(to bottom, #CE1126 15%, #1e40af 15%, #1e40af 85%, #CE1126 85%)';
      p.style.padding = '14px'; /* Border thickness */
      p.style.boxSizing = 'border-box';
      
      let inner = document.createElement('div');
      inner.style.height = '100%';
      inner.style.width = '100%';
      inner.style.background = '#ffffff';
      inner.style.columnCount = '2';
      inner.style.columnGap = '7mm';
      inner.style.columnFill = 'auto';
      inner.style.overflow = 'hidden';
      inner.style.padding = '8mm 6mm';
      inner.style.boxSizing = 'border-box';
      inner.className = 'a4-inner-page';
      
      p.appendChild(inner);"""

code = code.replace(target, new_code)

# Now we need to change currentPage.appendChild(clone) to currentPage.firstChild.appendChild(clone)
# But wait, currentPage.scrollWidth is now inner.scrollWidth!

# Let's do a regex replacement for currentPage.append and currentPage.scrollWidth
code = re.sub(r'currentPage\.appendChild\((.*?)\);', r'currentPage.querySelector(".a4-inner-page").appendChild(\1);', code)
code = re.sub(r'currentPage\.removeChild\((.*?)\);', r'currentPage.querySelector(".a4-inner-page").removeChild(\1);', code)
code = re.sub(r'currentPage\.scrollWidth', r'currentPage.querySelector(".a4-inner-page").scrollWidth', code)
code = re.sub(r'currentPage\.clientWidth', r'currentPage.querySelector(".a4-inner-page").clientWidth', code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Changed border implementation to background wrapper for reliable 4-sided borders")
