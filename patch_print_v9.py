import re

with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. @page margin to 0 to put border at absolute edge and auto-hide headers/footers
css = re.sub(
    r'@page\s*\{[^}]*\}',
    '@page {\n  size: A4;\n  margin: 0;\n}',
    css
)

# 2. Border is exactly at the edge, thickness 3mm
css = re.sub(
    r'body::before\s*\{[^}]*\}',
    '''body::before {
    content: "";
    position: fixed;
    top: 0; bottom: 0; left: 0; right: 0;
    border: 3mm solid;
    border-image: linear-gradient(to bottom, #ce1126 25%, #002868 25%, #002868 75%, #ce1126 75%) 1;
    z-index: 9999;
    pointer-events: none;
  }''',
    css
)

# 3. .letter padding for horizontal safety
css = re.sub(
    r'\.letter\s*\{[^}]*\}',
    '.letter {\n    border: none !important;\n    padding: 0 8mm !important;\n    max-width: none;\n    margin: 0;\n    background: transparent;\n    box-sizing: border-box;\n    width: 100%;\n  }',
    css
)

# 4. The Magic Page Break Inset Combo
patterns = [
    r'\.letter__text\s+p\s*\{[^}]*\}',
    r'\.letter__row\s*\{[^}]*\}',
    r'\.letter__figure\s*\{[^}]*\}',
    r'\.letter__text\s+\.subheading\s*\{[^}]*\}',
    r'\.letter__closing\s*\{[^}]*\}',
    r'\.letter__hero\s*\{[^}]*\}',
    r'\.letter__text\s+p,\s*\.letter__row,\s*\.letter__figure,\s*\.letter__text\s+\.subheading,\s*\.prayers,\s*\.letter__closing\s*\{[^}]*\}',
    r'\.letter__row\s*\.letter__figure\s*\{[^}]*\}'
]

for p in patterns:
    css = re.sub(p, '', css)

optimized_rules = """
  .letter__text p,
  .letter__row,
  .letter__figure,
  .letter__text .subheading,
  .prayers,
  .letter__closing {
    break-inside: avoid;
    page-break-inside: avoid;
    border-top: 4mm solid transparent;
    border-bottom: 4mm solid transparent;
    margin-top: -4mm;
    margin-bottom: -2mm;
    background-clip: padding-box;
  }
  
  .letter__row { display: flex; gap: 3mm; width: 100%; }
  .letter__row .letter__figure { flex: 1; min-width: 0; border: none; margin: 0; padding: 0; }
  
  .letter__text .subheading { font-size: 11pt; color: #004080; font-weight: bold; }
  .letter__closing { border-top: 1pt solid #ccc; font-size: 10pt; line-height: 1.5; color: #1a1a1a; text-align: justify; word-break: keep-all; }
  
  .letter__hero {
    display: block;
    height: auto;
    min-height: 0;
    margin: 0;
    border-top: 4mm solid transparent;
  }
"""

css = css.replace("/* 기도제목 (연두색 박스) */", optimized_rules + "\n  /* 기도제목 (연두색 박스) */")

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated print CSS to v9")
