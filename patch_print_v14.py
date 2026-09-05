import re

with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    css = f.read()

idx = css.find('@media print')
if idx != -1:
    css = css[:idx]

print_css = """
@media print {
  @page {
    size: A4;
    margin: 0;
  }
  
  :root { --bg: #fff; }
  body { background: #fff; font-size: 10.5pt; color: #1a1a1a; margin: 0; padding: 0; }
  .no-print, .nav, .sticky-bar, .reader-actions, .dialog-back, #toast, .lock, .letter-nav, .reader-foot { display: none !important; }

  /* Border is at absolute edge. 
     Top/bottom are 1mm (ultra thin) to minimize text overlap at page breaks.
     Left/right are 4mm (thick) for the main pillar look. */
  body::before {
    content: "";
    position: fixed;
    top: 0; bottom: 0; left: 0; right: 0;
    border-style: solid;
    border-width: 1.5mm 4mm; 
    border-image: linear-gradient(to bottom, #ce1126 25%, #002868 25%, #002868 75%, #ce1126 75%) 1;
    z-index: 9999;
    pointer-events: none;
  }

  .letter {
    border: none !important;
    padding: 0 8mm !important;
    max-width: none;
    margin: 0;
    background: transparent;
    box-sizing: border-box;
    width: 100%;
    column-count: 2;
    column-gap: 8mm;
    /* Removed translateZ to prevent Chrome column-fill bugs */
  }

  .support { display: none !important; }

  /* Standard, robust paragraph flow. No negative margin hacks! */
  .letter__text p {
    margin: 0 0 3.5mm;
    padding: 0;
    break-inside: auto;
    page-break-inside: auto;
    orphans: 2;
    widows: 2;
    line-height: 1.6;
  }

  .letter__row, .letter__figure, .prayers, .letter__closing {
    break-inside: avoid;
    page-break-inside: avoid;
    margin: 4mm 0;
  }
  
  .letter__row { display: flex; gap: 2mm; width: 100%; }
  .letter__row .letter__figure { flex: 1; min-width: 0; margin: 0; border: none; padding: 0; }
  
  .letter__text .subheading {
    break-after: avoid;
    page-break-after: avoid;
    font-size: 11pt; color: #004080; font-weight: bold;
    margin-top: 5mm; margin-bottom: 2mm;
  }
  
  .letter__closing { 
    font-size: 10.5pt; 
    line-height: 1.6; 
    color: #1a1a1a; 
    text-align: justify; 
    word-break: keep-all; 
    padding-top: 3mm;
    border-top: 1pt solid #ccc;
  }
  
  .letter__hero {
    display: block;
    height: auto;
    min-height: 0;
    margin: 0 0 8mm 0; /* Lots of space below hero image */
    padding-top: 12mm; /* Push hero well down from top border */
    break-inside: avoid;
    page-break-inside: avoid;
  }

  .prayers {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
    border: 1pt dashed #4caf50;
    padding: 4mm !important;
    background: #f1f8e9;
    border-radius: 8px;
  }
  .prayers__title { font-size: 13pt; color: #2e7d32; font-weight: bold; margin: 0 0 3mm; text-align: center; display: block; }
  .prayers__list { padding-left: 0; list-style: none; margin: 0; display: block; }
  .prayers__item { display: block; padding: 2mm 0; border-top: 1pt dashed #a5d6a7; margin-top: 1mm; }
  .prayers__item:first-child { border-top: none; padding-top: 0; margin-top: 0; }
  .prayers__item::before { content: counter(prayer) ". "; font-size: 11pt; color: #c62828; font-weight: bold; display: inline; }
  .prayers__name { font-size: 11pt; color: #c62828; font-weight: bold; margin: 0; display: inline; }
  .prayers__text { font-size: 10pt; color: #111; display: block; margin-top: 1.5mm; line-height: 1.5; text-align: left; }
  .prayers__text p { margin: 0 0 1mm; border: none; padding: 0; }

  /* Text shadow to protect text overlapping the 1.5mm border */
  .letter__body, .letter__closing {
    text-shadow: 
      -1px -1px 0 #fff,  
       1px -1px 0 #fff,
      -1px  1px 0 #fff,
       1px  1px 0 #fff,
       0px  2px 4px rgba(255,255,255,0.8);
  }

  .letter__hero--banner { height: auto; aspect-ratio: auto; }
  .letter__hero--banner img { position: relative; height: auto; }
  .letter__hero--banner .letter__hero-overlay,
  .letter__hero--banner .letter__hero-content { display: none !important; }
}
"""

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(css + print_css)

print("Updated print CSS to v14")
