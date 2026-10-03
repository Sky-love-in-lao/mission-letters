import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Fix typo "두손모아주세요요" to "두 손 모아 기도해 주세요" just in case it wasn't perfect
code = code.replace("두손모아주세요요", "두 손 모아 기도해 주세요")

# We need to modify the JS paginator loop to handle first paragraph, subheadings, hero image, and closing.
# Let's replace the whole printLetter function to be safe and clean.

target = re.search(r'export async function printLetter.*?setTimeout\(\(\) => \{.*?\}, 1000\);\n\}', code, re.DOTALL).group(0)

new_printLetter = """export async function printLetter(root, onStatus) {
  onStatus?.('사진을 불러오는 중입니다…');
  const { failed, total } = await loadLetterImages(root);
  await Promise.all(
    Array.from(root.querySelectorAll('img[data-drive-id]'))
      .filter(img => img.src && !img.dataset.driveFailed)
      .map(img => (img.decode ? img.decode().catch(() => {}) : Promise.resolve()))
  );
  onStatus?.(failed ? `사진 ${total}장 중 ${failed}장을 불러오지 못했습니다.` : '');
  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  
  onStatus?.('A4 2단 레이아웃 최적화 중...');
  
  const container = document.createElement('div');
  container.style.position = 'absolute';
  container.style.top = '-99999px';
  container.style.left = '-99999px';
  container.style.width = '210mm';
  container.classList.add('is-measuring-print');
  document.body.appendChild(container);

  const PAGE_HEIGHT_MM = 297;
  
  const sheet = root.querySelector('.letter__sheet');
  let currentBlocks = [];
  if (sheet) {
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
  }

  let bestScale = 1.0;
  let finalPages = [];
  
  for (let s = 1.0; s >= 0.50; s -= 0.04) {
    container.innerHTML = '';
    container.style.setProperty('--print-scale', s.toString());
    
    let pages = [];
    let pageIndex = 0;
    let isFirstParagraph = true;
    
    const createPage = () => {
      let p = document.createElement('div');
      p.className = 'a4-print-page';
      p.style.height = PAGE_HEIGHT_MM + 'mm';
      p.style.width = '100%';
      p.style.position = 'relative';
      p.style.background = 'linear-gradient(to bottom, #CE1126 15%, #1e40af 15%, #1e40af 85%, #CE1126 85%)';
      p.style.padding = '12px';
      p.style.boxSizing = 'border-box';
      
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
        }
        
        const title = header.querySelector('.letter__title');
        if (title) {
          title.style.margin = '0 0 2mm 0';
        }
        
        currentPage.querySelector(".a4-inner-page").appendChild(header);
      }
    }
    container.appendChild(currentPage);
    pages.push(currentPage);

    for (const block of currentBlocks) {
      const clone = block.cloneNode(true);
      if (clone.style) {
        clone.style.maxWidth = '100%';
        clone.style.boxSizing = 'border-box';
        
        if (clone.classList.contains('letter__text')) {
           const pTag = clone.querySelector('p');
           if (pTag) {
             pTag.style.fontSize = (10 * s) + 'pt';
             pTag.style.margin = '0 0 1.5mm 0';
             pTag.style.lineHeight = '1.4';
             
             // First Bible verse red and bold
             if (isFirstParagraph) {
               pTag.style.color = '#dc2626';
               pTag.style.fontWeight = 'bold';
               isFirstParagraph = false;
             }
             
             // Subheadings
             const sub = pTag.querySelector('.subheading');
             if (sub) {
               pTag.style.marginTop = '4mm';
               pTag.style.marginBottom = '1mm';
             }
           }
        }
        if (clone.classList.contains('letter__row')) {
           clone.style.margin = '1mm 0';
           clone.style.gap = '1mm';
        }
        if (clone.classList.contains('prayers')) {
           clone.querySelectorAll('.prayers__subtitle').forEach(el => el.style.fontSize = (11 * s) + 'pt');
           clone.querySelectorAll('.prayers__text').forEach(el => el.style.fontSize = (10 * s) + 'pt');
           clone.style.marginTop = '4mm';
        }
      }
      
      currentPage.querySelector(".a4-inner-page").appendChild(clone);
      
      if (currentPage.querySelector(".a4-inner-page").scrollWidth > currentPage.querySelector(".a4-inner-page").clientWidth + 15) {
        currentPage.querySelector(".a4-inner-page").removeChild(clone);
        pageIndex++;
        currentPage = createPage();
        container.appendChild(currentPage);
        pages.push(currentPage);
        currentPage.querySelector(".a4-inner-page").appendChild(clone);
      }
    }
    
    if (pages.length <= 2 || s < 0.55) {
      bestScale = s;
      finalPages = pages.map(p => p.cloneNode(true));
      break;
    }
  }
  
  document.body.removeChild(container);
  
  root.innerHTML = '';
  root.style.border = 'none';
  root.style.padding = '0';
  root.style.maxWidth = '100%';
  
  for (const page of finalPages) {
    page.style.setProperty('--print-scale', bestScale.toString());
    page.style.breakAfter = 'page';
    page.style.pageBreakAfter = 'always';
    page.style.margin = '0 auto';
    root.appendChild(page);
  }
  
  document.documentElement.style.setProperty('--print-scale', bestScale.toString());
  document.body.style.setProperty('--print-scale', bestScale.toString());
  
  onStatus?.('');
  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  window.print();
  
  setTimeout(() => {
    document.documentElement.style.removeProperty('--print-scale');
    document.body.style.removeProperty('--print-scale');
  }, 1000);
}"""

code = code.replace(target, new_printLetter)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V12 patches: hero image, first verse, subheading gaps, closing scale")
