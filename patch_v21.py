import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Revert the disastrous height: 100%; overflow: hidden; from html, body
target_inject = """    @media print {
      html, body { margin: 0 !important; padding: 0 !important; height: 100% !important; overflow: hidden !important; }"""
new_inject = """    @media print {
      html, body { margin: 0 !important; padding: 0 !important; }"""
code = code.replace(target_inject, new_inject)

# Also, put back pageBreakAfter: always! 
# Since I removed overflow: hidden, without explicit breaks Chrome might do weird things.
# BUT wait, the box-shadow is inside 100vh. If we use pageBreakAfter, it might create a blank page.
# Actually, if we use pageBreakAfter: always, it creates a blank page IF the element is exactly 100vh.
# The safest way is to use height: 297mm instead of 100vh, and use pageBreakAfter: always.
# BUT height: 297mm split into 2 pages before!
# Let's try height: 296mm WITH pageBreakAfter: always!
# Since we use box-shadow inset, the border won't be cut off even if it's 296mm!
# Let's just restore pageBreakAfter: always but keep 100vh. No, 100vh + pageBreakAfter = 4 pages.
# Let's change 100vh to 296mm, and RESTORE pageBreakAfter!

target_break = """    // REMOVED pageBreakAfter: always. 
    // Since height is 100vh, natural flow will perfectly paginate without creating blank pages!
    page.style.breakAfter = 'auto';
    page.style.pageBreakAfter = 'auto';"""
new_break = """    if (i < finalPages.length - 1) {
      page.style.breakAfter = 'page';
      page.style.pageBreakAfter = 'always';
    } else {
      page.style.breakAfter = 'auto';
      page.style.pageBreakAfter = 'auto';
    }"""
code = code.replace(target_break, new_break)

code = code.replace("page.style.height = '100vh';", "page.style.height = '296mm';")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V21 patches: removed body overflow hidden, restored pageBreakAfter, used 296mm height")
