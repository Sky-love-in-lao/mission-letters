import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the block parsing logic to fix letter__closing disappearing
target_parsing = """  if (sheet) {
    for (const block of Array.from(sheet.children)) {
      if (block.classList.contains('letter__body') || block.classList.contains('letter__closing')) {
        for (const textBlock of Array.from(block.children)) {
          if (textBlock.classList.contains('letter__text') || block.classList.contains('letter__closing')) {
            for (const p of Array.from(textBlock.children)) {
              const wrapper = document.createElement('div');
              wrapper.className = 'letter__text';
              wrapper.appendChild(p.cloneNode(true));
              currentBlocks.push(wrapper);
            }
          } else {
            currentBlocks.push(textBlock);
          }
        }
      } else {
        currentBlocks.push(block);
      }
    }
  }"""

new_parsing = """  if (sheet) {
    for (const block of Array.from(sheet.children)) {
      if (block.classList.contains('letter__body')) {
        for (const textBlock of Array.from(block.children)) {
          if (textBlock.classList.contains('letter__text')) {
            for (const p of Array.from(textBlock.children)) {
              const wrapper = document.createElement('div');
              wrapper.className = 'letter__text';
              wrapper.appendChild(p.cloneNode(true));
              currentBlocks.push(wrapper);
            }
          } else {
            currentBlocks.push(textBlock);
          }
        }
      } else if (block.classList.contains('letter__closing')) {
        // Closing text is just a bunch of <p> tags inside .letter__closing
        for (const p of Array.from(block.children)) {
          const wrapper = document.createElement('div');
          wrapper.className = 'letter__text';
          wrapper.appendChild(p.cloneNode(true));
          currentBlocks.push(wrapper);
        }
      } else {
        currentBlocks.push(block);
      }
    }
  }"""

code = code.replace(target_parsing, new_parsing)


# Fix hero image cropping and position, and page width/height
target_page = """    const createPage = () => {
      let p = document.createElement('div');
      p.className = 'a4-print-page';
      p.style.height = PAGE_HEIGHT_MM + 'mm';
      p.style.width = '100%';
      p.style.position = 'relative';
      p.style.background = 'linear-gradient(to bottom, #CE1126 15%, #1e40af 15%, #1e40af 85%, #CE1126 85%)';
      p.style.padding = '12px';
      p.style.boxSizing = 'border-box';
      p.style.overflow = 'hidden';
      
      let inner = document.createElement('div');
      inner.style.height = '100%';
      inner.style.width = '100%';
      inner.style.background = '#ffffff';
      inner.style.columnCount = '2';
      inner.style.columnGap = '7mm';
      inner.style.columnFill = 'auto';
      inner.style.overflow = 'hidden';
      inner.style.padding = '8mm 6mm';
      inner.style.boxSizing = 'border-box';
      inner.className = 'a4-inner-page';
      
      p.appendChild(inner);
      return p;
    };

    let currentPage = createPage();
    if (pageIndex === 0) {
      const head = root.querySelector('.letter__head, .letter__hero');
      if (head) {
        const header = head.cloneNode(true);
        header.style.columnSpan = 'all';
        header.style.marginBottom = '2mm';
        
        // Hero Image adjustments
        const heroImg = header.querySelector('img');
        if (heroImg) {
          heroImg.style.maxHeight = '35mm';
          heroImg.style.width = 'auto';
          heroImg.style.margin = '0 auto';
          heroImg.style.display = 'block';
        }"""

new_page = """    const createPage = () => {
      let p = document.createElement('div');
      p.className = 'a4-print-page';
      p.style.height = '295mm'; // Slightly smaller to prevent 4 page spillover
      p.style.width = '208mm';  // Slightly smaller to prevent right border cutoff
      p.style.position = 'relative';
      p.style.background = 'linear-gradient(to bottom, #CE1126 15%, #1e40af 15%, #1e40af 85%, #CE1126 85%)';
      p.style.padding = '12px';
      p.style.boxSizing = 'border-box';
      p.style.overflow = 'hidden';
      p.style.margin = '0 auto';
      
      let inner = document.createElement('div');
      inner.style.height = '100%';
      inner.style.width = '100%';
      inner.style.background = '#ffffff';
      inner.style.columnCount = '2';
      inner.style.columnGap = '7mm';
      inner.style.columnFill = 'auto';
      inner.style.overflow = 'hidden';
      inner.style.padding = '4mm 6mm 8mm 6mm'; // Reduced top padding to move hero image up
      inner.style.boxSizing = 'border-box';
      inner.className = 'a4-inner-page';
      
      p.appendChild(inner);
      return p;
    };

    let currentPage = createPage();
    if (pageIndex === 0) {
      const head = root.querySelector('.letter__head, .letter__hero');
      if (head) {
        const header = head.cloneNode(true);
        header.style.columnSpan = 'all';
        header.style.marginBottom = '2mm';
        header.style.marginTop = '0';
        
        // Hero Image adjustments to prevent cropping and push to top
        const heroImg = header.querySelector('img');
        if (heroImg) {
          heroImg.style.maxHeight = '40mm';
          heroImg.style.width = '100%';
          heroImg.style.objectFit = 'contain'; // Prevent cropping!
          heroImg.style.margin = '0';
          heroImg.style.display = 'block';
        }
        
        // Also fix the hero container just in case
        const heroFig = header.querySelector('.letter__hero, .letter__hero-photo');
        if (heroFig) {
            heroFig.style.margin = '0';
            heroFig.style.padding = '0';
        }"""

# Need to handle missing target due to missing overflow: hidden in original target. Let's use regex.
code = re.sub(r'const createPage = \(\) => \{.*?if \(heroImg\) \{[^\}]*\}', new_page, code, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V13 patches to render_v2.js")
