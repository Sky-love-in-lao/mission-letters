import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. REMOVE the manual page break logic completely! This was crashing the scale 's' to 0.54!
target_loop = """           // Force page break before "노아의 눈치작전"
           if (pTag && pTag.textContent.includes('노아의 눈치작전')) {
               if (currentPage.querySelector(".a4-inner-page").children.length > 0) {
                   pageIndex++;
                   currentPage = createPage();
                   container.appendChild(currentPage);
                   pages.push(currentPage);
               }
           }"""
code = code.replace(target_loop, "")

# 2. RESTORE 100vh and 100% to fix the white gaps (weird borders)
code = code.replace("page.style.height = '1122px'; // EXACTLY 1px under Chrome A4 pixel height to prevent overflow blank pages!", "page.style.height = '100vh';")
code = code.replace("page.style.width = '793px'; // EXACTLY under A4 pixel width", "page.style.width = '100%';")

# 3. Ensure Prayer font sizes are large. (They are currently 22, 18, 15.5 which is great). Let's boost text slightly to 16.5 just to be safe.
code = code.replace("el.style.fontSize = (15.5 * s) + 'pt';", "el.style.fontSize = (16.5 * s) + 'pt';")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V24 patches: removed manual break (fixes tiny font), restored 100vh (fixes border)")
