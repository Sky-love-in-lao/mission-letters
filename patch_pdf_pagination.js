import fs from 'fs';

let renderCode = fs.readFileSync('assets/js/render_v2.js', 'utf-8');

// We need to replace printLetter function with a robust pagination logic.
const newPrintLetter = `export async function printLetter(root, onStatus) {
  onStatus?.('사진을 불러오는 중입니다…');
  const { failed, total } = await loadLetterImages(root);
  await Promise.all(
    Array.from(root.querySelectorAll('img[data-drive-id]'))
      .filter(img => img.src && !img.dataset.driveFailed)
      .map(img => (img.decode ? img.decode().catch(() => {}) : Promise.resolve()))
  );
  onStatus?.(failed ? \`사진 \${total}장 중 \${failed}장을 불러오지 못했습니다.\` : '');
  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  
  onStatus?.('A4 2단 레이아웃 생성 중...');
  
  // Create a hidden container for pagination
  const container = document.createElement('div');
  container.style.position = 'absolute';
  container.style.top = '-9999px';
  container.style.left = '-9999px';
  container.style.width = '180mm'; // A4 width minus margins (210 - 15 - 15)
  container.style.background = '#fff';
  container.classList.add('is-measuring-print');
  document.body.appendChild(container);

  const PAGE_HEIGHT_MM = 267; // 297 - 15 - 15
  
  // Extract all block elements from the letter
  const blocks = Array.from(root.querySelector('.letter__sheet').children);
  let currentBlocks = [];
  
  // Expand composite blocks (like .letter__body which contains paragraphs)
  for (const block of blocks) {
    if (block.classList.contains('letter__body')) {
      currentBlocks.push(...Array.from(block.children));
    } else {
      currentBlocks.push(block);
    }
  }

  // We want to scale down if it exceeds 2 pages
  let bestScale = 1.0;
  let finalPages = [];
  
  for (let s = 1.0; s >= 0.65; s -= 0.05) {
    container.innerHTML = '';
    container.style.setProperty('--print-scale', s.toString());
    
    let pages = [];
    let pageIndex = 0;
    
    let currentPage = document.createElement('div');
    currentPage.style.height = PAGE_HEIGHT_MM + 'mm';
    currentPage.style.columnCount = '2';
    currentPage.style.columnGap = '7mm';
    currentPage.style.columnFill = 'auto';
    currentPage.style.overflow = 'hidden';
    currentPage.style.position = 'relative';
    // Add border to the page to match reference
    currentPage.style.border = '12px solid transparent';
    currentPage.style.borderImage = 'linear-gradient(to bottom, #CE1126 15%, #1e40af 15%, #1e40af 85%, #CE1126 85%) 1';
    currentPage.style.padding = '4mm';
    currentPage.style.boxSizing = 'border-box';
    currentPage.style.marginBottom = '20px';
    
    // Add header to first page
    if (pageIndex === 0) {
      const header = root.querySelector('.letter__head, .letter__hero').cloneNode(true);
      header.style.columnSpan = 'all'; // Span across columns
      currentPage.appendChild(header);
    }
    
    container.appendChild(currentPage);
    pages.push(currentPage);

    for (const block of currentBlocks) {
      const clone = block.cloneNode(true);
      currentPage.appendChild(clone);
      
      // Check if adding this block caused an overflow (column 3 created)
      // Since it's column-count: 2, if scrollWidth > clientWidth, it overflowed horizontally
      if (currentPage.scrollWidth > currentPage.clientWidth + 5) {
        currentPage.removeChild(clone); // Remove it
        
        // Create new page
        pageIndex++;
        currentPage = document.createElement('div');
        currentPage.style.height = PAGE_HEIGHT_MM + 'mm';
        currentPage.style.columnCount = '2';
        currentPage.style.columnGap = '7mm';
        currentPage.style.columnFill = 'auto';
        currentPage.style.overflow = 'hidden';
        currentPage.style.position = 'relative';
        currentPage.style.border = '12px solid transparent';
        currentPage.style.borderImage = 'linear-gradient(to bottom, #CE1126 15%, #1e40af 15%, #1e40af 85%, #CE1126 85%) 1';
        currentPage.style.padding = '4mm';
        currentPage.style.boxSizing = 'border-box';
        currentPage.style.marginBottom = '20px';
        
        container.appendChild(currentPage);
        pages.push(currentPage);
        
        currentPage.appendChild(clone);
      }
    }
    
    if (pages.length <= 2 || s < 0.7) {
      bestScale = s;
      finalPages = pages.map(p => p.cloneNode(true));
      break;
    }
  }
  
  document.body.removeChild(container);
  
  // Now replace the content of root with our paginated pages!
  root.innerHTML = '';
  root.style.border = 'none'; // Remove original border, pages have it
  root.style.padding = '0';
  root.style.maxWidth = '100%';
  
  for (const page of finalPages) {
    page.style.marginBottom = '0'; // For actual printing, let @page handle margins
    page.style.breakAfter = 'page';
    page.style.pageBreakAfter = 'always';
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
}`;

renderCode = renderCode.replace(/export async function printLetter[\s\S]*?setTimeout\(\(\) => \{[\s\S]*?\}, 1000\);\n\}/m, newPrintLetter);

fs.writeFileSync('assets/js/render_v2.js', renderCode);
console.log('Paginated printLetter injected!');
