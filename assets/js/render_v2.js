// 편지 본문 렌더링 — 보기 화면과 작성 미리보기, 인쇄가 모두 같은 결과를 쓰도록 한 곳에 둔다.
// 디자인: Sacred Correspondence — Hero(첫 사진) → 에디토리얼 교차 배치 → 기도제목 → 후원 안내.

import { esc, paragraphs, periodLabel } from './util.js';
import { loadDriveImage, driveViewUrl, SHARE_HELP } from './drive_v2.js';

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
const HERO_SIZES  = ['short', 'normal', 'tall'];

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
        <h1 class="letter__title">${esc(body.title || '선교편지')}</h1>
        ${body.authorName ? `<p class="letter__author">${esc(body.authorName)}</p>` : ''}
      </div>
    </header>`;
}

function plainHeadHTML(body) {
  return `
    <header class="letter__head">
      <h1 class="letter__title">${esc(body.title || '선교편지')}</h1>
      ${body.authorName ? `<p class="letter__author">${esc(body.authorName)}</p>` : ''}
    </header>`;
}

function prayersHTML(prayers, id) {
  const items = (prayers || []).filter(p => String(p?.title || p?.text || '').trim());
  if (!items.length) return '';
  return `
    <section class="prayers">
      <h2 class="prayers__title">🙏 두 손 모아 ㄱ도해 주세요</h2>
      <ol class="prayers__list">
        ${items.map((p, i) => `
          <li class="prayers__item">
            ${p.title ? `<h3 class="prayers__name">${esc(p.title)}</h3>` : ''}
            ${p.text ? `<div class="prayers__text">${paragraphs(p.text)}</div>` : ''}
          </li>`).join('')}
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
      ${s.note ? `<div class="support__note">${paragraphs(s.note)}</div>` : ''}
      ${rows.length ? `
        <dl class="support__account">
          ${rows.map(([label, value]) => `
            <div class="support__row">
              <dt>${esc(label)}</dt>
              <dd>${esc(value)}</dd>
            </div>`).join('')}
        </dl>` : ''}
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
      ${heroSrc ? heroHTML(heroSrc, heroSize, body) : plainHeadHTML(body)}
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
export async function printLetter(root, onStatus) {
  onStatus?.('사진을 불러오는 중입니다…');
  const { failed, total } = await loadLetterImages(root);
  // 디코딩까지 끝나야 인쇄에 반영된다.
  await Promise.all(
    Array.from(root.querySelectorAll('img[data-drive-id]'))
      .filter(img => img.src && !img.dataset.driveFailed)
      .map(img => (img.decode ? img.decode().catch(() => {}) : Promise.resolve()))
  );
  onStatus?.(failed ? `사진 ${total}장 중 ${failed}장을 불러오지 못했습니다.` : '');
  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  window.print();
}
