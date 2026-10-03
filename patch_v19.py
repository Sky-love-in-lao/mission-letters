import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix 4-page bug using inset box-shadow instead of borders
target_page = """    // Prevent 4-page Chrome split bug using 100vh
    page.style.position = 'relative';
    page.style.height = '100vh';
    page.style.width = '100%';
    page.style.breakInside = 'avoid';
    page.style.pageBreakInside = 'avoid';"""

new_page = """    // Prevent 4-page Chrome split bug using 100vh
    page.style.position = 'relative';
    page.style.height = '100vh';
    page.style.width = '100%';
    page.style.breakInside = 'avoid';
    page.style.pageBreakInside = 'avoid';
    // Use inset box-shadow for borders so it NEVER expands the 100vh height!
    page.style.boxShadow = 'inset 0 14px 0 0 #CE1126, inset 0 -14px 0 0 #CE1126';
    page.style.borderTop = 'none';
    page.style.borderBottom = 'none';"""

code = code.replace(target_page, new_page)

# Also remove the old borderTop/borderBottom from the createPage function
target_create_borders = """      p.style.borderTop = '12px solid #CE1126';    // GUARANTEED red top
      p.style.borderBottom = '12px solid #CE1126'; // GUARANTEED red bottom"""
new_create_borders = """      p.style.borderTop = 'none'; 
      p.style.borderBottom = 'none';"""
code = code.replace(target_create_borders, new_create_borders)


# 2. Force manual page break for "노아의 눈치작전"
target_loop = """        if (clone.classList.contains('letter__text')) {
           const pTag = clone.querySelector('p');"""

new_loop = """        if (clone.classList.contains('letter__text')) {
           const pTag = clone.querySelector('p');
           
           // Force page break before "노아의 눈치작전"
           if (pTag && pTag.textContent.includes('노아의 눈치작전')) {
               pageIndex++;
               currentPage = createPage();
               container.appendChild(currentPage);
               pages.push(currentPage);
           }"""
code = code.replace(target_loop, new_loop)


# 3. Massively increase Prayer Box font sizes and spacing
target_prayers = """           clone.querySelectorAll('.prayers__subtitle').forEach(el => el.style.fontSize = (15.5 * s) + 'pt');
           clone.querySelectorAll('.prayers__text').forEach(el => el.style.fontSize = (14.5 * s) + 'pt');
           clone.style.marginTop = '4mm';
           clone.style.breakBefore = 'column'; // Force it to the right column!
           clone.style.pageBreakBefore = 'always'; // Fallback
        }"""

new_prayers = """           clone.querySelectorAll('.prayers__title').forEach(el => el.style.fontSize = (22 * s) + 'pt');
           clone.querySelectorAll('.prayers__subtitle').forEach(el => {
               el.style.fontSize = (18 * s) + 'pt';
               el.style.lineHeight = '1.4';
               el.style.display = 'block';
               el.style.marginBottom = '4px';
           });
           clone.querySelectorAll('.prayers__text').forEach(el => {
               el.style.fontSize = (15.5 * s) + 'pt';
               el.style.lineHeight = '1.6';
           });
           clone.querySelectorAll('.print-prayer-item').forEach(el => el.style.marginBottom = '22px');
           
           clone.style.marginTop = '2mm';
           clone.style.breakBefore = 'column'; // Force it to the right column!
           clone.style.pageBreakBefore = 'always'; // Fallback
        }"""
code = code.replace(target_prayers, new_prayers)

# Ensure prayers__title can be targeted
code = code.replace("clone.querySelectorAll('.prayers__title')", "clone.querySelectorAll('.prayers__title, .print-prayer-title-wrapper')")


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V19 patches: box-shadow borders, manual page break, massive prayer fonts")
