import sys, re

file_path = 'assets/js/render_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Clean up "01. " from prayer titles in JS directly to avoid CSS caching issues
target_prayers = """            <strong class="prayers__subtitle print-prayer-num">${i + 1}. ${esc(p.title || '')}</strong>"""
new_prayers = """            <strong class="prayers__subtitle print-prayer-num">${i + 1}. ${esc((p.title || '').replace(/^\\d+\\.\\s*/, ''))}</strong>"""
code = code.replace(target_prayers, new_prayers)

# 2. Fix the Border to guarantee top/bottom, and Force Prayer to right column
target_page = """      p.style.height = '295mm'; // Slightly smaller to prevent 4 page spillover
      p.style.width = '208mm';  // Slightly smaller to prevent right border cutoff
      p.style.position = 'relative';
      p.style.background = 'linear-gradient(to bottom, #CE1126 15%, #1e40af 15%, #1e40af 85%, #CE1126 85%)';
      p.style.padding = '12px';
      p.style.boxSizing = 'border-box';
      p.style.overflow = 'hidden';
      p.style.margin = '0 auto';"""

new_page = """      p.style.height = '295mm'; 
      p.style.width = '208mm';  
      p.style.position = 'relative';
      p.style.background = 'linear-gradient(to bottom, #CE1126 15%, #1e40af 15%, #1e40af 85%, #CE1126 85%)';
      p.style.borderTop = '12px solid #CE1126';    // GUARANTEED red top
      p.style.borderBottom = '12px solid #CE1126'; // GUARANTEED red bottom
      p.style.padding = '0 12px';                  // Side padding reveals gradient
      p.style.boxSizing = 'border-box';
      p.style.overflow = 'hidden';
      p.style.margin = '0 auto';"""
code = code.replace(target_page, new_page)


target_clone_prayers = """        if (clone.classList.contains('prayers')) {
           clone.querySelectorAll('.prayers__subtitle').forEach(el => el.style.fontSize = (11 * s) + 'pt');
           clone.querySelectorAll('.prayers__text').forEach(el => el.style.fontSize = (10 * s) + 'pt');
           clone.style.marginTop = '4mm';
        }"""

new_clone_prayers = """        if (clone.classList.contains('prayers')) {
           clone.querySelectorAll('.prayers__subtitle').forEach(el => el.style.fontSize = (11 * s) + 'pt');
           clone.querySelectorAll('.prayers__text').forEach(el => el.style.fontSize = (10 * s) + 'pt');
           clone.style.marginTop = '4mm';
           clone.style.breakBefore = 'column'; // Force it to the right column!
           clone.style.pageBreakBefore = 'always'; // Fallback
        }"""
code = code.replace(target_clone_prayers, new_clone_prayers)


# 3. Inject CSS dynamically in printLetter to bypass ServiceWorker cache!
target_inject = """  onStatus?.('A4 2단 레이아웃 최적화 중...');
  
  const container = document.createElement('div');"""

new_inject = """  onStatus?.('A4 2단 레이아웃 최적화 중...');
  
  // Inject CSS dynamically to bypass aggressive ServiceWorker caching
  let styleEl = document.getElementById('dynamic-print-css');
  if (!styleEl) {
    styleEl = document.createElement('style');
    styleEl.id = 'dynamic-print-css';
    document.head.appendChild(styleEl);
  }
  styleEl.innerHTML = `
    @media print {
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
      .print-prayer-item::before {
        display: none !important;
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

  const container = document.createElement('div');"""

code = code.replace(target_inject, new_inject)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V14 patches: solid borders, force right column, dynamic CSS injection")
