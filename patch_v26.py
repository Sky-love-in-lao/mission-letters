import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix the tiny font bug by removing pageBreakBefore: always from the Prayer Box!
target_prayers = """           clone.style.breakBefore = 'column'; // Force it to the right column!
           clone.style.pageBreakBefore = 'always'; // Fallback"""
new_prayers = """           clone.style.breakBefore = 'column'; // Force it to the next column safely!"""
code = code.replace(target_prayers, new_prayers)

# 2. Increase prayer fonts even more!
code = code.replace("el.style.fontSize = (16.5 * s) + 'pt';", "el.style.fontSize = (18.5 * s) + 'pt';")
code = code.replace("el.style.fontSize = (18 * s) + 'pt';", "el.style.fontSize = (20 * s) + 'pt';")
code = code.replace("el.style.fontSize = (22 * s) + 'pt';", "el.style.fontSize = (26 * s) + 'pt';")
code = code.replace("el.style.marginBottom = '22px';", "el.style.marginBottom = '30px';")

# 3. Fix 4-page bug AND red square borders AND white gaps!
target_page = """    // Prevent 4-page Chrome split bug using 100vh
    page.style.position = 'relative';
    page.style.height = '100vh';
    page.style.width = '100%';
    page.style.breakInside = 'avoid';
    page.style.pageBreakInside = 'avoid';
    // Use inset box-shadow for borders so it NEVER expands the 100vh height!
    page.style.boxShadow = 'inset 0 14px 0 0 #CE1126, inset 0 -14px 0 0 #CE1126';
    page.style.borderTop = 'none';
    page.style.borderBottom = 'none';"""

new_page = """    // Ultimate 2-page border fix
    page.style.position = 'relative';
    page.style.height = '1122px'; // Exact pixel height slightly under A4 to prevent blank pages
    page.style.width = '793px';
    page.style.boxSizing = 'border-box';
    page.style.breakInside = 'avoid';
    page.style.pageBreakInside = 'avoid';
    page.style.borderTop = '14px solid #CE1126';
    page.style.borderBottom = '14px solid #CE1126';
    page.style.boxShadow = 'none'; // Fixes red square corners!"""
code = code.replace(target_page, new_page)

# Update the print CSS to mask any sub-pixel white gaps at the bottom with red background
target_css = """    @media print {
      html, body { margin: 0 !important; padding: 0 !important; }"""
new_css = """    @media print {
      html, body { 
         margin: 0 !important; 
         padding: 0 !important; 
         background-color: #CE1126 !important;
         -webkit-print-color-adjust: exact;
      }"""
code = code.replace(target_css, new_css)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V26 patches: fixed pageBreakBefore bug causing tiny fonts, fixed red squares, increased prayer size")
