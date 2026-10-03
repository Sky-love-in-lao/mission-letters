import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

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
  container.style.width = '180mm';
  container.classList.add('is-measuring-print');
  document.body.appendChild(container);

  const PAGE_HEIGHT_MM = 267;
  
  const sheet = root.querySelector('.letter__sheet');
  let currentBlocks = [];
  if (sheet) {
    for (const block of Array.from(sheet.children)) {
      if (block.classList.contains('letter__body')) {
        currentBlocks.push(...Array.from(block.children));
      } else {
        currentBlocks.push(block);
      }
    }
  }

  let bestScale = 1.0;
  let finalPages = [];
  
  for (let s = 1.0; s >= 0.60; s -= 0.04) {
    container.innerHTML = '';
    container.style.setProperty('--print-scale', s.toString());
    
    let pages = [];
    let pageIndex = 0;
    
    const createPage = () => {
      let p = document.createElement('div');
      p.className = 'a4-print-page';
      p.style.height = PAGE_HEIGHT_MM + 'mm';
      p.style.columnCount = '2';
      p.style.columnGap = '7mm';
      p.style.columnFill = 'auto';
      p.style.overflow = 'hidden';
      p.style.position = 'relative';
      p.style.border = '12px solid transparent';
      p.style.borderImage = 'linear-gradient(to bottom, #CE1126 15%, #1e40af 15%, #1e40af 85%, #CE1126 85%) 1';
      p.style.padding = '0 4mm';
      p.style.boxSizing = 'border-box';
      return p;
    };

    let currentPage = createPage();
    if (pageIndex === 0) {
      const head = root.querySelector('.letter__head, .letter__hero');
      if (head) {
        const header = head.cloneNode(true);
        header.style.columnSpan = 'all';
        currentPage.appendChild(header);
      }
    }
    container.appendChild(currentPage);
    pages.push(currentPage);

    for (const block of currentBlocks) {
      const clone = block.cloneNode(true);
      currentPage.appendChild(clone);
      
      if (currentPage.scrollWidth > currentPage.clientWidth + 5 || currentPage.scrollHeight > currentPage.clientHeight + 5) {
        currentPage.removeChild(clone);
        pageIndex++;
        currentPage = createPage();
        container.appendChild(currentPage);
        pages.push(currentPage);
        currentPage.appendChild(clone);
      }
    }
    
    if (pages.length <= 2 || s < 0.65) {
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
}
"""

code = re.sub(r'export async function printLetter[\s\S]*?setTimeout\(\(\) => \{[\s\S]*?\}, 1000\);\n\}', new_printLetter, code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Paginated printLetter injected with python!")
