import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target_prayers = """function prayersHTML(prayers, id) {
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
}"""

new_prayers = """function prayersHTML(prayers, id) {
  const items = (prayers || []).filter(p => String(p?.title || p?.text || '').trim());
  if (!items.length) return '';
  return `
    <section class="prayers print-prayer-box">
      <div class="print-prayer-title-wrapper">
        <h2 class="prayers__title">두손모아주세요요</h2>
      </div>
      <ol class="prayers__list print-prayer-list">
        ${items.map((p, i) => `
          <li class="prayers__item print-prayer-item">
            <strong class="prayers__subtitle print-prayer-num">${i + 1}. ${esc(p.title || '')}</strong>
            <p class="prayers__text print-prayer-desc">${esc(p.text || '')}</p>
          </li>
        `).join('')}
      </ol>
    </section>`;
}"""

code = code.replace(target_prayers, new_prayers)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Patched prayersHTML")
