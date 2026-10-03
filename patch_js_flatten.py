import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = """  if (sheet) {
    for (const block of Array.from(sheet.children)) {
      if (block.classList.contains('letter__body')) {
        currentBlocks.push(...Array.from(block.children));
      } else {
        currentBlocks.push(block);
      }
    }
  }"""

new_code = """  if (sheet) {
    for (const block of Array.from(sheet.children)) {
      if (block.classList.contains('letter__body')) {
        // Flatten text blocks to individual paragraphs for perfect pagination
        for (const textBlock of Array.from(block.children)) {
          if (textBlock.classList.contains('letter__text')) {
            currentBlocks.push(...Array.from(textBlock.children));
          } else {
            currentBlocks.push(textBlock);
          }
        }
      } else {
        currentBlocks.push(block);
      }
    }
  }"""

code = code.replace(target, new_code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Flattened text blocks for perfect pagination")
