import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Restore supportHTML
target_html = """      ${body.closing ? `<div class="letter__closing">${paragraphs(body.closing)}</div>` : ''}
    </article>
  `;"""

new_html = """      ${body.closing ? `<div class="letter__closing">${paragraphs(body.closing)}</div>` : ''}
      ${supportHTML(body.support)}
    </article>
  `;"""

if "supportHTML(body.support)" not in code:
    code = code.replace(target_html, new_html)

# 2. Revert photo shrinking from v16
target_clone = """        if (clone.classList.contains('letter__row')) {
           clone.style.margin = '0';
           clone.style.gap = '1mm';
           clone.querySelectorAll('img').forEach(img => {
               img.style.maxHeight = '35mm'; // Shrink photos to allow much larger text!
               img.style.width = 'auto';
               img.style.objectFit = 'contain';
           });
        }"""

new_clone = """        if (clone.classList.contains('letter__row')) {
           clone.style.margin = '1mm 0';
           clone.style.gap = '1mm';
        }"""
code = code.replace(target_clone, new_clone)

target_hero = """          heroImg.style.maxHeight = '28mm';"""
new_hero = """          heroImg.style.maxHeight = '40mm';"""
code = code.replace(target_hero, new_hero)

# 3. Ultimate 4-page fix: Absolute positioning for pages
target_append = """  for (let i = 0; i < finalPages.length; i++) {
    const page = finalPages[i];
    page.style.setProperty('--print-scale', bestScale.toString());
    
    // Prevent 4-page Chrome split bug
    page.style.height = '100vh';
    page.style.breakInside = 'avoid';
    page.style.pageBreakInside = 'avoid';
    
    if (i < finalPages.length - 1) {
      page.style.breakAfter = 'page';
      page.style.pageBreakAfter = 'always';
    } else {
      page.style.breakAfter = 'auto';
      page.style.pageBreakAfter = 'auto';
    }
    page.style.margin = '0 auto';
    root.appendChild(page);
  }"""

new_append = """  
  // Ultimate 4-page bug fix: Absolute positioning
  root.style.position = 'relative';
  root.style.height = (finalPages.length * 297) + 'mm';
  
  for (let i = 0; i < finalPages.length; i++) {
    const page = finalPages[i];
    page.style.setProperty('--print-scale', bestScale.toString());
    
    page.style.position = 'absolute';
    page.style.top = (i * 297) + 'mm';
    page.style.left = '0';
    page.style.width = '210mm';
    page.style.height = '297mm';
    
    page.style.breakInside = 'avoid';
    page.style.pageBreakInside = 'avoid';
    page.style.breakAfter = 'auto';
    page.style.pageBreakAfter = 'auto';
    page.style.margin = '0';
    
    root.appendChild(page);
  }"""

code = code.replace(target_append, new_append)

# Also fix the page creation to be exactly 297mm
code = code.replace("p.style.height = '295mm';", "p.style.height = '297mm';")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V17 patches: Restore supportHTML, revert photos, Absolute Positioning print pages")
