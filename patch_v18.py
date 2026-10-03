import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Restore supportHTML CORRECTLY!
target_html = """        ${body.closing ? `<div class="letter__closing">${paragraphs(body.closing)}</div>` : ''}
        ${prayersHTML(body.prayers, meta.id)}
        
      </div>"""

new_html = """        ${body.closing ? `<div class="letter__closing">${paragraphs(body.closing)}</div>` : ''}
        ${prayersHTML(body.prayers, meta.id)}
        ${supportHTML(body.support)}
      </div>"""

if "supportHTML(body.support)" not in code:
    code = code.replace(target_html, new_html)

# 2. Revert Absolute Positioning, go back to 100vh
target_append = """  // Ultimate 4-page bug fix: Absolute positioning
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

new_append = """  
  for (let i = 0; i < finalPages.length; i++) {
    const page = finalPages[i];
    page.style.setProperty('--print-scale', bestScale.toString());
    
    // Prevent 4-page Chrome split bug using 100vh
    page.style.position = 'relative';
    page.style.height = '100vh';
    page.style.width = '100%';
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

code = code.replace(target_append, new_append)

# Also fix the page creation to be 100vh initially just in case? No, the loop needs absolute mm to calculate layout.
# It uses 297mm. That's fine.

# 3. Increase Prayer Font Sizes significantly!
target_fonts = """           clone.querySelectorAll('.prayers__subtitle').forEach(el => el.style.fontSize = (13 * s) + 'pt');
           clone.querySelectorAll('.prayers__text').forEach(el => el.style.fontSize = (12 * s) + 'pt');"""
new_fonts = """           clone.querySelectorAll('.prayers__subtitle').forEach(el => el.style.fontSize = (15.5 * s) + 'pt');
           clone.querySelectorAll('.prayers__text').forEach(el => el.style.fontSize = (14.5 * s) + 'pt');"""
code = code.replace(target_fonts, new_fonts)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V18 patches: Restore supportHTML correctly, revert to 100vh, huge prayer fonts")
