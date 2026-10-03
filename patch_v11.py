import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove support section from letterHTML
code = re.sub(r'\$\{supportHTML\(body\.support\)\}', '', code)

# 2. Update prayersHTML to match the Green Box format
target_prayers = """function prayersHTML(prayers, id) {
  const items = (prayers || []).filter(p => String(p?.title || p?.text || '').trim());
  if (!items.length) return '';
  return `
    <section class="prayers" aria-labelledby="${id}-prayers">
      <h2 id="${id}-prayers" class="prayers__title">🙏 두 손 모아 ㄱ도해 주세요</h2>
      <ol class="prayers__list">
        ${items.map(p => `
          <li class="prayers__item">
            ${p.title ? `<strong class="prayers__subtitle">${esc(p.title)}</strong>` : ''}
            <p class="prayers__text">${esc(p.text || '')}</p>
          </li>
        `).join('')}
      </ol>
    </section>`;
}"""

new_prayers = """function prayersHTML(prayers, id) {
  const items = (prayers || []).filter(p => String(p?.title || p?.text || '').trim());
  if (!items.length) return '';
  return `
    <section class="prayers" aria-labelledby="${id}-prayers" style="background-color: #f0fdf4; border: 1px solid #166534; padding: 15px; margin-top: 10px;">
      <div style="background-color: #fff; border: 1px solid #166534; padding: 4px 8px; display: inline-block; margin-bottom: 10px;">
        <h2 id="${id}-prayers" class="prayers__title" style="margin: 0; font-size: 14pt; color: #000; font-weight: 800;">두 손 모아 ㄱ도해 주세요</h2>
      </div>
      <ol class="prayers__list" style="list-style: none; padding: 0; margin: 0;">
        ${items.map((p, i) => `
          <li class="prayers__item" style="margin-bottom: 8px;">
            <strong class="prayers__subtitle" style="color: #dc2626; font-size: 11pt;">${i + 1}. ${esc(p.title || '')}</strong>
            <p class="prayers__text" style="margin: 2px 0 0 0; font-size: 10pt; color: #000; line-height: 1.4;">${esc(p.text || '')}</p>
          </li>
        `).join('')}
      </ol>
    </section>`;
}"""

code = code.replace(target_prayers, new_prayers)

# 3. Fix JS Paginator logic (width, height, inline fonts, spacing)
# Find the newPrintLetter function body and replace it.
# We will use regex to find the loop and fix it.

target_paginator_setup = """      p.style.height = PAGE_HEIGHT_MM + 'mm';
      p.style.width = '210mm';
      p.style.position = 'relative';
      p.style.background = 'linear-gradient(to bottom, #CE1126 15%, #1e40af 15%, #1e40af 85%, #CE1126 85%)';
      p.style.padding = '14px'; /* Border thickness */"""

new_paginator_setup = """      p.style.height = '296mm';
      p.style.width = '100%';
      p.style.position = 'relative';
      p.style.background = 'linear-gradient(to bottom, #CE1126 15%, #1e40af 15%, #1e40af 85%, #CE1126 85%)';
      p.style.padding = '12px'; /* Slightly thinner border to save space */"""

code = code.replace(target_paginator_setup, new_paginator_setup)

# Force apply styles directly to cloned nodes to guarantee font scaling and margin reduction
target_clone = """      const clone = block.cloneNode(true);
      if (clone.style) {
        clone.style.maxWidth = '100%';
        clone.style.boxSizing = 'border-box';
      }
      currentPage.querySelector(".a4-inner-page").appendChild(clone);"""

new_clone = """      const clone = block.cloneNode(true);
      if (clone.style) {
        clone.style.maxWidth = '100%';
        clone.style.boxSizing = 'border-box';
        
        // Hardcode font size to guarantee scaling works in Chrome Print
        if (clone.classList.contains('letter__text')) {
           const pTag = clone.querySelector('p');
           if (pTag) {
             pTag.style.fontSize = (10 * s) + 'pt';
             pTag.style.margin = '0 0 1.5mm 0'; // Reduce paragraph spacing
             pTag.style.lineHeight = '1.4';
           }
        }
        if (clone.classList.contains('letter__row')) {
           clone.style.margin = '1mm 0'; // Reduce photo gap
           clone.style.gap = '1mm';
        }
        if (clone.classList.contains('prayers')) {
           // scale prayers text
           clone.querySelectorAll('.prayers__subtitle').forEach(el => el.style.fontSize = (11 * s) + 'pt');
           clone.querySelectorAll('.prayers__text').forEach(el => el.style.fontSize = (10 * s) + 'pt');
        }
      }
      currentPage.querySelector(".a4-inner-page").appendChild(clone);"""

code = code.replace(target_clone, new_clone)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V11 patches: green prayers, no support, 100% width, explicit font sizes")
