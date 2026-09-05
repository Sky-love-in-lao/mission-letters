import re

with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    css = f.read()

start_idx = css.find('/* ── A4 인쇄 — PRD §6.3 ───────────────────────────────────────── */')

if start_idx == -1:
    print("Could not find print section")
    exit(1)

new_print_css = """/* ── A4 인쇄 — PRD §6.3 ───────────────────────────────────────── */
@page {
  size: A4;
  margin: 0;
}

@media print {
  :root { --bg: #fff; }
  body { background: #fff; font-size: 10.5pt; color: #1a1a1a; margin: 0; padding: 0; }
  .no-print, .nav, .sticky-bar, .reader-actions, .dialog-back, #toast, .lock, .letter-nav, .reader-foot { display: none !important; }

  /* 모든 페이지 사면을 채우는 라오스 국기 테두리 */
  body::before {
    content: "";
    position: fixed;
    top: 8mm; bottom: 8mm; left: 8mm; right: 8mm;
    border: 2.5mm solid;
    border-image: linear-gradient(to bottom, #ce1126 25%, #002868 25%, #002868 75%, #ce1126 75%) 1;
    z-index: 9999;
    pointer-events: none;
  }

  .page, .page--reader { max-width: none; margin: 0; padding: 0; }

  .letter {
    border: none !important;
    padding: 16mm 15mm !important;
    max-width: none;
    margin: 0;
    background: transparent;
    box-sizing: border-box;
    width: 100%;
  }

  .letter__head {
    border-bottom: 1.5pt solid #cc0000;
    margin-bottom: 6mm;
    padding-bottom: 4mm;
    text-align: center;
  }

  .masthead { display: none; }

  /* 배너 이미지 인쇄 최적화 */
  .letter__hero {
    display: block;
    height: auto;
    min-height: 0;
    margin-bottom: 6mm;
    padding-bottom: 0;
    border: none;
    background: none;
    break-inside: avoid;
  }
  .letter__hero-photo {
    width: 100%;
    height: auto;
    max-height: 60mm;
    object-fit: contain;
  }
  
  /* 배너형일 때는 배경 장막과 HTML 텍스트를 숨김 (이미지에 글자가 있으므로) */
  .letter__hero--banner .letter__hero-veil,
  .letter__hero--banner .letter__hero-text {
    display: none !important;
  }
  
  /* 일반 사진일 때는 장막만 숨기고 텍스트는 인쇄에 맞게 검은색으로 표시 */
  .letter__hero:not(.letter__hero--banner) .letter__hero-veil { display: none !important; }
  .letter__hero:not(.letter__hero--banner) .letter__hero-text { padding: 0; text-align: center; }
  .letter__hero:not(.letter__hero--banner) .letter__title { color: #1a1a1a; text-shadow: none; font-size: 22pt; margin-top: 4mm; font-weight: bold; }
  .letter__hero:not(.letter__hero--banner) .letter__author { color: #555; text-shadow: none; font-size: 11pt; margin-top: 2mm; }

  .letter__title { font-size: 22pt; color: #1a1a1a; text-align: center; font-weight: bold; margin-bottom: 2mm; }
  .letter__period { display: inline-block; font-size: 12pt; color: #1a1a1a; margin-bottom: 2mm; margin-right: 5mm; }
  .letter__author { display: inline-block; font-size: 12pt; color: #1a1a1a; margin-bottom: 2mm; }
  
  /* 2단 편집 레이아웃 */
  .letter__sheet {
    column-count: 2;
    column-gap: 8mm;
  }

  .letter__greeting { font-size: 12pt; margin-bottom: 5mm; color: #cc0000; font-weight: bold; text-align: center; }
  
  .letter__body { font-size: 10.5pt; line-height: 1.6; text-align: justify; word-break: keep-all; }
  .letter__text p { margin: 0 0 3mm; orphans: 2; widows: 2; }
  .letter__text strong { font-weight: 700; color: #000; }
  .letter__text .subheading { display: block; font-size: 11.5pt; color: #004080; font-weight: bold; margin-top: 4mm; margin-bottom: 1.5mm; }

  .letter__row {
    display: flex;
    gap: 3mm;
    margin: 4mm 0;
    break-inside: avoid;
    page-break-inside: avoid;
    width: 100%;
  }
  .letter__row .letter__figure {
    flex: 1;
    min-width: 0;
    margin: 0;
  }
  .letter__photo { max-width: 100%; height: auto; max-height: 80mm; object-fit: contain; }

  .letter__figure {
    margin: 4mm 0;
    break-inside: avoid;
    page-break-inside: avoid;
    width: 100%;
  }
  .letter__figure figcaption { font-size: 9pt; color: #555; text-align: center; margin-top: 1.5mm; }
  .letter__figure.is-failed { display: none; }

  .letter__closing { margin-top: 6mm; padding-top: 4mm; border-top: 1pt solid #ccc; font-size: 10pt; color: #333; text-align: justify; word-break: keep-all; }

  /* 기도제목 (연두색 박스) */
  .prayers {
    margin-top: 8mm;
    padding: 5mm;
    border: 2pt solid #4caf50;
    background: #f1f8e9;
    break-inside: avoid;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .prayers__title { font-size: 13pt; color: #2e7d32; font-weight: bold; margin: 0 0 3mm; text-align: center; display: block; }
  .prayers__list { padding-left: 0; list-style: none; margin: 0; display: block; }
  .prayers__item { 
    display: block; 
    padding: 2mm 0; 
    border-top: 1pt dashed #a5d6a7; 
    margin-top: 1mm; 
  }
  .prayers__item:first-child { border-top: none; padding-top: 0; margin-top: 0; }
  
  .prayers__item::before {
    content: counter(prayer) ". ";
    font-size: 11pt; color: #c62828; font-weight: bold; display: inline;
  }
  .prayers__name { font-size: 11pt; color: #c62828; font-weight: bold; margin: 0; display: inline; }
  .prayers__text { font-size: 10pt; color: #111; display: block; margin-top: 1.5mm; line-height: 1.5; text-align: left; }
  .prayers__text p { margin: 0 0 1mm; }
  
  /* 불필요한 그리드 속성 덮어쓰기 */
  .prayers__item > * { grid-column: auto; }

  .support {
    margin-top: 6mm; padding-top: 4mm; border-top: 1pt solid #ccc; break-inside: avoid;
  }
  .support__title { font-size: 11pt; font-weight: bold; color: #1a2b45; margin: 0 0 2mm; }
  .support__account { display: block; margin: 0; }
  .support__row { display: block; padding: 1mm 0; font-size: 10pt; border-bottom: 1pt dotted #ccc; }
  .support__row dt { display: inline; font-weight: bold; }
  .support__row dd { display: inline; margin-left: 2mm; }
  .support__note { font-size: 9pt; color: #555; margin-top: 2mm; }

  a { color: inherit; text-decoration: none; }
}

@media screen { .print-only { display: none !important; } }
"""

css = css[:start_idx] + new_print_css
with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated print CSS to v2")
