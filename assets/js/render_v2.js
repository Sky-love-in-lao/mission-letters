// 편지 본문 렌더링 — 보기 화면과 작성 미리보기, 인쇄가 모두 같은 결과를 쓰도록 한 곳에 둔다.
// 디자인: Sacred Correspondence — Hero(첫 사진) → 에디토리얼 교차 배치 → 기도제목 → 후원 안내.

import { esc, paragraphs, periodLabel } from './util.js?v=1788590728';
import { loadDriveImage, driveViewUrl, SHARE_HELP } from './drive_v2.js?v=1788590728';

const PRAYED_KEY = (id, i) => `missionletter.prayed.${id}.${i}`;

/** 경로·URL 이면 그대로 싣고, 맨 파일 ID 면 드라이브에서 불러온다. */
function imageTag(value, className, alt) {
  const src = String(value || '').trim();
  if (!src) return '';
  return /[/.]/.test(src)
    ? `<img class="${className}" src="${esc(src)}" alt="${esc(alt)}">`
    : `<img class="${className}" data-drive-id="${esc(src)}" alt="${esc(alt)}" referrerpolicy="no-referrer">`;
}

const PHOTO_SIZES = ['small', 'normal', 'wide'];
const PER_ROW = [1, 2, 3];

/** 이 사진을 한 줄에 몇 장씩 놓을지 (기본 1장) */
function perRowOf(block) {
  const n = Number(block.perRow);
  return PER_ROW.includes(n) ? n : 1;
}
const HERO_SIZES  = ['banner', 'short', 'normal', 'tall'];

function sizeClass(prefix, value, allowed) {
  const size = allowed.includes(value) ? value : 'normal';
  return `${prefix}--${size}`;
}

function figureHTML(block, extraClass = '') {
  const imgSrc = block.image ? `<img src="${esc(block.image)}" class="letter__photo" alt="${esc(block.caption || '선교 사진')}">` :
    `<img class="letter__photo" data-drive-id="${esc(block.driveId)}" alt="${esc(block.caption || '선교 사진')}" referrerpolicy="no-referrer">`;
  const href = block.image ? esc(block.image) : esc(driveViewUrl(block.driveId));
  return `
    <figure class="letter__figure ${extraClass}">
      <a href="${href}" target="_blank" rel="noopener noreferrer">
        ${imgSrc}
      </a>
      <div class="letter__photo-fallback" hidden>${SHARE_HELP}</div>
      ${block.caption ? `<figcaption>${esc(block.caption)}</figcaption>` : ''}
    </figure>`;
}

function mastheadHTML(body, period) {
  if (!period) return '';

  return `
    <div class="masthead masthead--bare">
      <div class="masthead__period">${esc(period)}</div>
    </div>`;
}

/** 머리말 — 머리글 사진 위에 제목을 얹는다(Hero). */
function heroHTML(src, size, body) {
  const isPath = /[/.]/.test(src);
  const photo = isPath
    ? `<img class="letter__hero-photo" src="${esc(src)}" alt="">`
    : `<a class="letter__hero-link" href="${esc(driveViewUrl(src))}" target="_blank" rel="noopener noreferrer" tabindex="-1" aria-hidden="true">
         <img class="letter__hero-photo" data-drive-id="${esc(src)}" alt="" referrerpolicy="no-referrer">
       </a>`;
  return `
    <header class="letter__hero ${sizeClass('letter__hero', size, HERO_SIZES)}">
      ${photo}
      <div class="letter__photo-fallback" hidden>${SHARE_HELP}</div>
      <div class="letter__hero-veil" aria-hidden="true"></div>
      <div class="letter__hero-text">
        ${period ? `<div class="letter__period print-only">${esc(period)}</div>` : ''}
      <h1 class="letter__title">${esc(body.title || '선교편지')}</h1>
        ${body.authorName ? `<p class="letter__author">${esc(body.authorName)}</p>` : ''}
      </div>
    </header>`;
}

function plainHeadHTML(body, period) {
  return `
    <header class="letter__head">
      ${period ? `<div class="letter__period print-only">${esc(period)}</div>` : ''}
      <h1 class="letter__title">${esc(body.title || '선교편지')}</h1>
      ${body.authorName ? `<p class="letter__author">${esc(body.authorName)}</p>` : ''}
    </header>`;
}

function prayersHTML(prayers, id) {
  const items = (prayers || []).filter(p => String(p?.title || p?.text || '').trim());
  if (!items.length) return '';
  return `
    <section class="prayers print-prayer-box">
      <div class="print-prayer-title-wrapper">
        <h2 class="prayers__title">ㄱ도해 주세요!</h2>
      </div>
      <ol class="prayers__list print-prayer-list">
        ${items.map((p, i) => `
          <li class="prayers__item print-prayer-item">
            <strong class="prayers__subtitle print-prayer-num" style="color: #dc2626;">${esc((p.title || '').replace(/^[\d\s\.]*(라0스|물가|자녀|영육)/, '$1'))}</strong>
            <p class="prayers__text print-prayer-desc">${esc(p.text || '')}</p>
          </li>
        `).join('')}
      </ol>
    </section>`;
}

function supportHTML(support) {
  const s = support || {};
  const rows = [
    s.bank    ? ['은행',   s.bank]    : null,
    s.account ? ['계좌번호', s.account] : null,
    s.holder  ? ['예금주', s.holder]  : null
  ].filter(Boolean);
  if (!rows.length && !String(s.note || '').trim()) return '';

  return `
    <section class="support">
      <h2 class="support__title">사역에 동참하기</h2>
      ${rows.length ? `
        <dl class="support__account">
          ${rows.map(([label, value]) => `
            <div class="support__row">
              <dt>${esc(label)}</dt>
              <dd>${esc(value)}</dd>
            </div>`).join('')}
        </dl>` : ''}
      ${s.note ? `<div class="support__note">${paragraphs(s.note)}</div>` : ''}
    </section>`;
}

function signoffHTML(body) {
  const photo = imageTag(body.portrait, 'letter__signoff-photo', body.authorName || '보내는 이');
  const name = String(body.authorName || '').trim();
  if (!photo && !name) return '';
  return `
    <div class="letter__signoff">
      ${photo}
      ${name ? `<p class="letter__signoff-name">${esc(name)}</p>` : ''}
    </div>`;
}

/** 편지 한 통을 HTML 로. 사진은 자리만 잡고 loadLetterImages() 에서 실제로 싣는다. */
export function letterHTML(body, meta = {}) {
  const period = body.period || periodLabel(meta.id);
  const all = body.blocks || [];

  // 머리글 사진. 옛 편지는 본문 첫 사진을 머리글로 썼으므로 그것도 받아 준다.
  const heroField = String(body.hero || '').trim();
  const legacy = !heroField && all[0]?.type === 'image' && all[0].driveId ? all[0] : null;
  const heroSrc = heroField || legacy?.driveId || '';
  const heroSize = heroField ? body.heroSize : legacy?.size;
  const rest = legacy ? all.slice(1) : all;

  // 연달아 놓인 사진 중 '한 줄에 몇 장'이 같은 것끼리 묶어 한 줄로 만든다.
  const parts = [];
  let i = 0;
  while (i < rest.length) {
    const block = rest[i];

    if (block.type === 'image' && (block.driveId || block.image)) {
      const per = perRowOf(block);
      const run = [];
      while (i < rest.length
             && rest[i].type === 'image' && (rest[i].driveId || rest[i].image)
             && perRowOf(rest[i]) === per) {
        run.push(rest[i]);
        i++;
      }
      if (per === 1) {
        run.forEach(photo => parts.push(figureHTML(photo, sizeClass('letter__figure', photo.size, PHOTO_SIZES))));
      } else {
        for (let k = 0; k < run.length; k += per) {
          const chunk = run.slice(k, k + per);
          parts.push(`<div class="letter__row letter__row--${per}">${
            chunk.map(photo => figureHTML(photo, 'letter__figure--tile')).join('')
          }</div>`);
        }
      }
      continue;
    }

    if (block.type === 'text' && String(block.value || '').trim()) {
      parts.push(`<div class="letter__text">${paragraphs(block.value)}</div>`);
    }
    i++;
  }
  const blocks = parts.join('');

  return `
    <article class="letter${heroSrc ? ' letter--hero' : ''}">
      ${mastheadHTML(body, period)}
      ${heroSrc ? heroHTML(heroSrc, heroSize, body) : plainHeadHTML(body, period)}
      <div class="letter__sheet">
        <div class="letter__body">${blocks}</div>
        ${body.closing ? `<div class="letter__closing">${paragraphs(body.closing)}</div>` : ''}
        ${prayersHTML(body.prayers, meta.id)}
        ${supportHTML(body.support)}
      </div>
    </article>`;
}

/**
 * '기도했습니다' — 서버가 없으므로 이 기기에서만 표시를 남긴다.
 * 선교사에게 전달되지 않는다는 점을 문구로 분명히 한다.
 */
export function bindPrayers(root) {
  // 기도 버튼이 제거되었으므로 더 이상 바인딩하지 않음
}

/**
 * 렌더된 편지 안의 드라이브 사진을 모두 싣는다.
 * @returns {Promise<{total:number, failed:number}>} 인쇄 전 대기용으로도 쓴다.
 */
export async function loadLetterImages(root) {
  const images = Array.from(root.querySelectorAll('img[data-drive-id]'));
  const results = await Promise.all(images.map(async img => {
    const result = await loadDriveImage(img, img.dataset.driveId);
    if (!result.ok) {
      const holder = img.closest('.letter__figure, .letter__hero, .masthead, .letter__signoff');
      holder?.classList.add('is-failed');
      const fallback = holder?.querySelector('.letter__photo-fallback');
      if (fallback) fallback.hidden = false;
    }
    return result.ok;
  }));
  return { total: images.length, failed: results.filter(ok => !ok).length };
}

/**
 * A4 인쇄 — PRD §6.3
 * 사진 로딩이 끝나기 전에 print() 를 부르면 사진 없는 PDF 가 만들어진다. 반드시 기다린다.
 */
export async function printLetter(root, onStatus, isPreview = false) {
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
  
  // Inject CSS dynamically to bypass aggressive ServiceWorker caching
  let styleEl = document.getElementById('dynamic-print-css');
  if (!styleEl) {
    styleEl = document.createElement('style');
    styleEl.id = 'dynamic-print-css';
    document.head.appendChild(styleEl);
  }
  styleEl.innerHTML = `
    @media print {
      html, body { 
         margin: 0 !important; 
         padding: 0 !important; 
         background-color: #CE1126 !important;
         -webkit-print-color-adjust: exact;
      }
      .print-prayer-box {
        background-color: #f0fdf4 !important;
        border: 1px solid #166534 !important;
        padding: 15px !important;
        margin-top: 10px !important;
        break-inside: avoid !important;
        display: block !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
      .print-prayer-title-wrapper {
        background-color: #fff !important;
        border: 1px solid #166534 !important;
        padding: 4px 8px !important;
        display: inline-block !important;
        margin-bottom: 10px !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
      .print-prayer-box .prayers__title {
        margin: 0 !important;
        font-size: calc(13pt * var(--print-scale, 1)) !important;
        color: #000 !important;
        font-weight: 800 !important;
      }
      .print-prayer-list {
        list-style: none !important;
        padding: 0 !important;
        margin: 0 !important;
        display: block !important;
      }
      .print-prayer-item {
        margin-bottom: 8px !important;
        display: block !important;
      }

      .print-prayer-num {
        color: #dc2626 !important;
        font-size: calc(10pt * var(--print-scale, 1)) !important;
        font-weight: bold !important;
        display: block !important;
      }
      .print-prayer-desc {
        margin: 2px 0 0 0 !important;
        font-size: calc(9pt * var(--print-scale, 1)) !important;
        color: #000 !important;
        line-height: 1.4 !important;
      }
      .support { display: none !important; }
    }
  `;

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
  }

  let bestScale = 1.0;
  let finalPages = [];
  
  for (let s = 1.0; s >= 0.50; s -= 0.02) {
    container.innerHTML = '';
    container.style.setProperty('--print-scale', s.toString());
    
    let pages = [];
    let pageIndex = 0;
    let isFirstParagraph = true;
    
        const createPage = () => {
      let p = document.createElement('div');
      p.className = 'a4-print-page';
      p.style.height = '297mm'; 
      p.style.width = '100%';  
      p.style.position = 'relative';
      p.style.background = 'linear-gradient(to bottom, #CE1126 15%, #1e40af 15%, #1e40af 85%, #CE1126 85%)';
      p.style.borderTop = 'none'; 
      p.style.borderBottom = 'none';
      p.style.padding = '0 12px';                  // Side padding reveals gradient
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
          heroImg.style.maxHeight = '32mm';
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
             pTag.style.fontSize = (14 * s) + 'pt';
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
           clone.style.padding = '8px 12px'; // Extreme shrink box padding
           clone.querySelectorAll('.prayers__title, .print-prayer-title-wrapper').forEach(el => {
               el.style.fontSize = (30 * s) + 'pt';
               el.style.marginBottom = '6px';
           });
           clone.querySelectorAll('.prayers__subtitle').forEach(el => {
               el.style.fontSize = (22 * s) + 'pt';
               el.style.lineHeight = '1.1'; // Extremely tight line height
               el.style.display = 'block';
               el.style.marginBottom = '1px';
           });
           clone.querySelectorAll('.prayers__text').forEach(el => {
               el.style.fontSize = (20 * s) + 'pt';
               el.style.lineHeight = '1.25'; // Extremely tight line height
           });
           clone.querySelectorAll('.print-prayer-item').forEach(el => el.style.marginBottom = '6px'); // Extreme margin reduction!
           
           clone.style.marginTop = '2mm';
           clone.style.breakBefore = 'column'; // Force it to the next column safely!
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
  
  
  
  for (let i = 0; i < finalPages.length; i++) {
    const page = finalPages[i];
    page.style.setProperty('--print-scale', bestScale.toString());
    
    // Ultimate 2-page border fix
    page.style.position = 'relative';
    page.style.height = '1122px'; // Exact pixel height slightly under A4 to prevent blank pages
    page.style.width = '793px';
    page.style.boxSizing = 'border-box';
    page.style.breakInside = 'avoid';
    page.style.pageBreakInside = 'avoid';
    page.style.borderTop = '14px solid #CE1126';
    page.style.borderBottom = '14px solid #CE1126';
    page.style.boxShadow = 'none'; // Fixes red square corners!
    
    page.style.breakAfter = 'auto';
    page.style.pageBreakAfter = 'auto';
    page.style.margin = '0 auto';
    
    root.appendChild(page);
  }
  
  document.documentElement.style.setProperty('--print-scale', bestScale.toString());
  document.body.style.setProperty('--print-scale', bestScale.toString());
  
  onStatus?.('');
  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  if (isPreview) {
      document.body.style.background = '#525659';
      document.body.style.padding = '20px';
      root.style.display = 'flex';
      root.style.flexDirection = 'column';
      root.style.gap = '20px';
      root.style.alignItems = 'center';
      for (const page of finalPages) {
          // Combine drop shadow with the inner red borders!
          page.style.boxShadow = '0 4px 12px rgba(0,0,0,0.5), inset 0 14px 0 0 #CE1126, inset 0 -14px 0 0 #CE1126';
          page.style.marginBottom = '20px';
      }
      return;
  }
  window.print();
  
  setTimeout(() => {
    document.documentElement.style.removeProperty('--print-scale');
    document.body.style.removeProperty('--print-scale');
  }, 1000);
}

