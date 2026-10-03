import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix the manual page break logic to NOT create empty pages
target_loop = """           // Force page break before "노아의 눈치작전"
           if (pTag && pTag.textContent.includes('노아의 눈치작전')) {
               pageIndex++;
               currentPage = createPage();
               container.appendChild(currentPage);
               pages.push(currentPage);
           }"""

new_loop = """           // Force page break before "노아의 눈치작전"
           if (pTag && pTag.textContent.includes('노아의 눈치작전')) {
               if (currentPage.querySelector(".a4-inner-page").children.length > 0) {
                   pageIndex++;
                   currentPage = createPage();
                   container.appendChild(currentPage);
                   pages.push(currentPage);
               }
           }"""
code = code.replace(target_loop, new_loop)

# 2. Fix the prayer numbers in the preview correctly.
# In v20 I replaced the HTML to have color: #dc2626 and removed the hardcoded number.
# But look at the user's v20 screenshot, it still says '01. 1. 라0스의...' !
# Why? Because they typed '01. ' or '1. ' in the input field!
# The regex `replace(/^\d+\.\s*/, '')` handles '1. ', but what if they typed '01. '?
# It handles '01. ' too!
# Why did it still say '01. 1. ' in the screenshot?
# Wait! In the screenshot, the RED text says "01." and the BLACK text says "1. 라0스의..."
# Ah! The RED text is the pseudo-element `::before` from CSS!
# The BLACK text is the actual HTML text!
# Why didn't the HTML text get stripped of "1. " ?
# Let's change the regex to be more aggressive!
code = code.replace("replace(/^\\d+\\.\\s*/, '')", "replace(/^[\\d\\s\\.]*(라0스|물가|자녀|영육)/, '$1')") 
# Actually, a better regex: `replace(/^[\d\s\.]+/g, '')` - strips ALL leading digits, spaces, and dots!
code = code.replace("replace(/^\\d+\\.\\s*/, '')", "replace(/^[\\d\\s\\.]+/g, '')")

# 3. For the 4-page fix, let's stick to 100vh and NO pageBreakAfter, because pageBreakAfter ALWAYS creates a blank page if the element is 100vh.
target_break = """    if (i < finalPages.length - 1) {
      page.style.breakAfter = 'page';
      page.style.pageBreakAfter = 'always';
    } else {
      page.style.breakAfter = 'auto';
      page.style.pageBreakAfter = 'auto';
    }"""
new_break = """    page.style.breakAfter = 'auto';
    page.style.pageBreakAfter = 'auto';"""
code = code.replace(target_break, new_break)

code = code.replace("page.style.height = '296mm';", "page.style.height = '100vh';")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V22 patches: fixed manual page break empty page bug, 100vh fix, strict regex for prayer numbers")
