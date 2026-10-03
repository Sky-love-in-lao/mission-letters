import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Fix 4-page bug by removing the final page break and using 100vh
target_append = """  for (const page of finalPages) {
    page.style.setProperty('--print-scale', bestScale.toString());
    page.style.breakAfter = 'page';
    page.style.pageBreakAfter = 'always';
    page.style.margin = '0 auto';
    root.appendChild(page);
  }"""

new_append = """  for (let i = 0; i < finalPages.length; i++) {
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

code = code.replace(target_append, new_append)


# Maximize font size by heavily restricting photo heights
target_clone = """        if (clone.classList.contains('letter__row')) {
           clone.style.margin = '1mm 0';
           clone.style.gap = '1mm';
        }"""

new_clone = """        if (clone.classList.contains('letter__row')) {
           clone.style.margin = '0';
           clone.style.gap = '1mm';
           clone.querySelectorAll('img').forEach(img => {
               img.style.maxHeight = '35mm'; // Shrink photos to allow much larger text!
               img.style.width = 'auto';
               img.style.objectFit = 'contain';
           });
        }"""

code = code.replace(target_clone, new_clone)


# Further shrink Hero Image to 25mm to save massive space
target_hero = """          heroImg.style.maxHeight = '40mm';"""
new_hero = """          heroImg.style.maxHeight = '28mm';"""
code = code.replace(target_hero, new_hero)

# Increase font sizes even more (base 12pt, prayers 14pt)
target_fonts1 = """pTag.style.fontSize = (11 * s) + 'pt';"""
new_fonts1 = """pTag.style.fontSize = (12.5 * s) + 'pt';"""
code = code.replace(target_fonts1, new_fonts1)

target_fonts2 = """           clone.querySelectorAll('.prayers__subtitle').forEach(el => el.style.fontSize = (13 * s) + 'pt');
           clone.querySelectorAll('.prayers__text').forEach(el => el.style.fontSize = (12 * s) + 'pt');"""
new_fonts2 = """           clone.querySelectorAll('.prayers__subtitle').forEach(el => el.style.fontSize = (14 * s) + 'pt');
           clone.querySelectorAll('.prayers__text').forEach(el => el.style.fontSize = (13 * s) + 'pt');"""
code = code.replace(target_fonts2, new_fonts2)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V16 patches: 100vh height, shrink photos, massive font size increase")
