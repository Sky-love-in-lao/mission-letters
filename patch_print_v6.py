import re

with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. @page margin
css = re.sub(
    r'@page\s*\{[^}]*\}',
    '@page {\n  size: A4;\n  margin: 12mm 10mm;\n}',
    css
)

# 2. .letter padding
css = re.sub(
    r'\.letter\s*\{[^}]*\}',
    '.letter {\n    border: none !important;\n    padding: 0 6mm !important;\n    max-width: none;\n    margin: 0;\n    background: transparent;\n    box-sizing: border-box;\n    width: 100%;\n  }',
    css
)

# 3. Convert vertical margins to padding
css = css.replace(
    ".letter__text p { margin: 0 0 3mm;",
    ".letter__text p { padding: 1.5mm 0; margin: 0;"
)
css = css.replace(
    ".letter__text .subheading { display: block; font-size: 11.5pt; color: #004080; font-weight: bold; margin-top: 4mm; margin-bottom: 1.5mm;",
    ".letter__text .subheading { display: block; font-size: 11.5pt; color: #004080; font-weight: bold; padding-top: 4mm; padding-bottom: 1.5mm; margin: 0;"
)
css = css.replace(
    ".letter__row {\n    display: flex;\n    gap: 3mm;\n    margin: 4mm 0;",
    ".letter__row {\n    display: flex;\n    gap: 3mm;\n    padding: 3mm 0;\n    margin: 0;"
)
css = css.replace(
    ".letter__figure {\n    margin: 4mm 0;",
    ".letter__figure {\n    padding: 3mm 0;\n    margin: 0;"
)
css = css.replace(
    ".letter__hero {\n    display: block;\n    margin-top: 4mm;\n    height: auto;\n    min-height: 0;\n    margin-bottom: 6mm;\n    padding-bottom: 0;",
    ".letter__hero {\n    display: block;\n    padding-top: 5mm;\n    padding-bottom: 5mm;\n    margin: 0;\n    height: auto;\n    min-height: 0;"
)
css = css.replace(
    ".letter__closing { margin-top: 6mm; padding-top: 4mm;",
    ".letter__closing { padding-top: 6mm; margin: 0;"
)

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated print CSS to v6")
