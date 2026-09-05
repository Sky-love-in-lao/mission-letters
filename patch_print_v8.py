import re

with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. @page margin to 4mm (hides headers/footers, border is at the absolute edge visually)
css = re.sub(
    r'@page\s*\{[^}]*\}',
    '@page {\n  size: A4;\n  margin: 4mm;\n}',
    css
)

# 2. Border to 2mm thick, exactly at the 4mm margin boundary
css = re.sub(
    r'body::before\s*\{[^}]*\}',
    '''body::before {
    content: "";
    position: fixed;
    top: 0; bottom: 0; left: 0; right: 0;
    border: 2mm solid;
    border-image: linear-gradient(to bottom, #ce1126 25%, #002868 25%, #002868 75%, #ce1126 75%) 1;
    z-index: 9999;
    pointer-events: none;
  }''',
    css
)

# 3. .letter horizontal padding to keep text away from side borders
css = re.sub(
    r'\.letter\s*\{[^}]*\}',
    '.letter {\n    border: none !important;\n    padding: 0 4mm !important;\n    max-width: none;\n    margin: 0;\n    background: transparent;\n    box-sizing: border-box;\n    width: 100%;\n  }',
    css
)

# 4. Minimize vertical padding to save space, but guarantee 2mm safe zone at page breaks
# Replace all previous padding/margin rules for these elements
patterns = [
    r'\.letter__text\s+p\s*\{[^}]*\}',
    r'\.letter__row\s*\{[^}]*\}',
    r'\.letter__figure\s*\{[^}]*\}',
    r'\.letter__text\s+\.subheading\s*\{[^}]*\}',
    r'\.letter__closing\s*\{[^}]*\}',
    r'\.letter__hero\s*\{[^}]*\}'
]

for p in patterns:
    css = re.sub(p, '', css)

# Append the new optimized rules
optimized_rules = """
  .letter__text p,
  .letter__row,
  .letter__figure,
  .letter__text .subheading,
  .prayers,
  .letter__closing {
    break-inside: avoid;
    page-break-inside: avoid;
    padding: 2mm 0;
    margin: 0;
  }
  
  .letter__row { display: flex; gap: 3mm; width: 100%; }
  .letter__row .letter__figure { flex: 1; min-width: 0; padding: 0; }
  
  .letter__text .subheading { font-size: 11.5pt; color: #004080; font-weight: bold; }
  .letter__closing { border-top: 1pt solid #ccc; font-size: 10.5pt; line-height: 1.6; color: #1a1a1a; text-align: justify; word-break: keep-all; }
  
  .letter__hero {
    display: block;
    height: auto;
    min-height: 0;
    padding-top: 2mm;
    padding-bottom: 2mm;
    margin: 0;
  }
"""

css = css.replace("/* 기도제목 (연두색 박스) */", optimized_rules + "\n  /* 기도제목 (연두색 박스) */")

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated print CSS to v8")
