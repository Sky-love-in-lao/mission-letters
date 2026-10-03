import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add isPreview parameter to printLetter
code = code.replace("export async function printLetter(root, onStatus) {", "export async function printLetter(root, onStatus, isPreview = false) {")

# 2. Prevent window.print() if isPreview is true, and style the body to look like a PDF viewer
target_print = """  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  window.print();
  
  setTimeout(() => {
    document.documentElement.style.removeProperty('--print-scale');
    document.body.style.removeProperty('--print-scale');
  }, 1000);"""

new_print = """  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  if (isPreview) {
      document.body.style.background = '#525659';
      document.body.style.padding = '20px';
      root.style.display = 'flex';
      root.style.flexDirection = 'column';
      root.style.gap = '20px';
      root.style.alignItems = 'center';
      for (const page of finalPages) {
          page.style.boxShadow = '0 4px 12px rgba(0,0,0,0.5)';
          page.style.marginBottom = '20px';
      }
      return;
  }
  window.print();
  
  setTimeout(() => {
    document.documentElement.style.removeProperty('--print-scale');
    document.body.style.removeProperty('--print-scale');
  }, 1000);"""
code = code.replace(target_print, new_print)


# 3. FIX THE 4-PAGE BUG FOR GOOD.
# If 100vh and 296mm both fail... Let's use 296mm AND height: 296mm!
# Wait, let's use exact A4 pixel dimensions for Chrome: 793.7px x 1122.5px.
# If we set height: 1122px, it is EXACTLY under the limit!
# And NO pageBreakAfter!
target_height = """page.style.height = '100vh';"""
new_height = """page.style.height = '1122px'; // EXACTLY 1px under Chrome A4 pixel height to prevent overflow blank pages!"""
code = code.replace(target_height, new_height)

target_width = """page.style.width = '100%';"""
new_width = """page.style.width = '793px'; // EXACTLY under A4 pixel width"""
code = code.replace(target_width, new_width)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V23 patches: isPreview flag, exact pixel dimensions for 4-page bug")
