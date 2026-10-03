import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix Prayer HTML: Remove hardcoded numbers, add red color
target_prayers = r"""<strong class="prayers__subtitle print-prayer-num">${i + 1}. ${esc((p.title || '').replace(/^\d+\.\s*/, ''))}</strong>"""
new_prayers = r"""<strong class="prayers__subtitle print-prayer-num" style="color: #dc2626;">${esc((p.title || '').replace(/^\d+\.\s*/, ''))}</strong>"""
code = code.replace(target_prayers, new_prayers)

# 2. Fix PDF CSS: Remove the rule that hides the counter!
target_css = """      .print-prayer-item::before {
        display: none !important;
      }"""
code = code.replace(target_css, "")

# 3. Fix 4-page Bug: Remove pageBreakAfter completely so 100vh doesn't generate blank pages!
target_break = """    if (i < finalPages.length - 1) {
      page.style.breakAfter = 'page';
      page.style.pageBreakAfter = 'always';
    } else {
      page.style.breakAfter = 'auto';
      page.style.pageBreakAfter = 'auto';
    }"""
new_break = """    // REMOVED pageBreakAfter: always. 
    // Since height is 100vh, natural flow will perfectly paginate without creating blank pages!
    page.style.breakAfter = 'auto';
    page.style.pageBreakAfter = 'auto';"""
code = code.replace(target_break, new_break)

# Also ensure html, body are 100% in print to avoid overflow
target_inject = """    @media print {"""
new_inject = """    @media print {
      html, body { margin: 0 !important; padding: 0 !important; height: 100% !important; overflow: hidden !important; }"""
code = code.replace(target_inject, new_inject)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V20 patches: removed pageBreakAfter for 4-page fix, fixed prayer numbers, added red subtitle")
