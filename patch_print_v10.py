import re

with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. @page margin to 0
css = re.sub(
    r'@page\s*\{[^}]*\}',
    '@page {\n  size: A4;\n  margin: 0;\n}',
    css
)

# 2. Border exactly at edge
css = re.sub(
    r'body::before\s*\{[^}]*\}',
    '''body::before {
    content: "";
    position: fixed;
    top: 0; bottom: 0; left: 0; right: 0;
    border: 3.5mm solid;
    border-image: linear-gradient(to bottom, #ce1126 25%, #002868 25%, #002868 75%, #ce1126 75%) 1;
    z-index: 9999;
    pointer-events: none;
  }''',
    css
)

# 3. Clean up the magic combo and huge padding/margins. Restore normal tight flow.
patterns = [
    r'\.letter__text\s+p,\s*\.letter__row,\s*\.letter__figure,\s*\.letter__text\s+\.subheading,\s*\.prayers,\s*\.letter__closing\s*\{[^}]*\}',
    r'\.letter__row\s*\{[^}]*\}',
    r'\.letter__row\s*\.letter__figure\s*\{[^}]*\}',
    r'\.letter__text\s+\.subheading\s*\{[^}]*\}',
    r'\.letter__closing\s*\{[^}]*\}',
    r'\.letter__hero\s*\{[^}]*\}'
]
for p in patterns:
    css = re.sub(p, '', css)

tight_rules = """
  /* Allow paragraphs to break to fix huge white spaces! */
  .letter__text p {
    margin: 0 0 1.5mm;
    padding: 0;
    break-inside: auto;
    page-break-inside: auto;
    orphans: 2;
    widows: 2;
  }
  
  /* Keep images and special blocks together */
  .letter__row, .letter__figure, .prayers, .letter__closing {
    break-inside: avoid;
    page-break-inside: avoid;
    margin: 1.5mm 0;
  }
  
  .letter__row { display: flex; gap: 2mm; width: 100%; }
  .letter__row .letter__figure { flex: 1; min-width: 0; margin: 0; }
  
  .letter__text .subheading {
    break-after: avoid;
    page-break-after: avoid;
    font-size: 11pt; color: #004080; font-weight: bold;
    margin-top: 3mm; margin-bottom: 1mm;
  }
  
  .letter__closing { border-top: 1pt solid #ccc; font-size: 10pt; line-height: 1.5; color: #1a1a1a; padding-top: 2mm; text-align: justify; word-break: keep-all; }
  
  .letter__hero {
    display: block;
    height: auto;
    min-height: 0;
    margin: 0 0 3mm 0;
    padding-top: 5mm; /* Safe space from top border on page 1 */
  }

  /* Add strong text-shadow to text so it remains readable if it overlaps the border at page breaks */
  .letter__body, .letter__closing, .prayers__text {
    text-shadow: 
      -1px -1px 0 #fff,  
       1px -1px 0 #fff,
      -1px  1px 0 #fff,
       1px  1px 0 #fff,
       0px  2px 4px rgba(255,255,255,0.8);
  }
"""

css = css.replace("/* 기도제목 (연두색 박스) */", tight_rules + "\n  /* 기도제목 (연두색 박스) */")

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated print CSS to v10")
