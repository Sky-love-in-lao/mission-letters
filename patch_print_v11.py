import re

with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. @page margin 0 is kept.
# 2. Border thickness: make top/bottom thinner (1.5mm) to minimize overlap, left/right thick (4mm)
css = re.sub(
    r'border:\s*3\.5mm\s*solid;',
    'border-style: solid;\n    border-width: 1.5mm 4mm;',
    css
)

# 3. Fix first page too high: increase padding-top on hero
css = css.replace(
    "padding-top: 5mm; /* Safe space from top border on page 1 */",
    "padding-top: 10mm; /* Safe space from top border on page 1 */"
)

# 4. Restore comfortable line-height and margins to fill 2 pages perfectly
css = css.replace(
    ".letter__text p {\n    margin: 0 0 1.5mm;\n    padding: 0;\n    break-inside: auto;\n    page-break-inside: auto;\n    orphans: 2;\n    widows: 2;\n  }",
    ".letter__text p {\n    margin: 0 0 3.5mm;\n    padding: 3mm 0;\n    margin-top: -3mm;\n    margin-bottom: 0.5mm;\n    -webkit-box-decoration-break: clone;\n    box-decoration-break: clone;\n    break-inside: auto;\n    page-break-inside: auto;\n    orphans: 3;\n    widows: 3;\n    line-height: 1.65;\n  }"
)

css = css.replace(
    ".letter__row, .letter__figure, .prayers, .letter__closing {\n    break-inside: avoid;\n    page-break-inside: avoid;\n    margin: 1.5mm 0;\n  }",
    ".letter__row, .letter__figure, .prayers, .letter__closing {\n    break-inside: avoid;\n    page-break-inside: avoid;\n    margin: 3.5mm 0;\n  }"
)

css = css.replace(
    ".letter__text .subheading {\n    break-after: avoid;\n    page-break-after: avoid;\n    font-size: 11pt; color: #004080; font-weight: bold;\n    margin-top: 3mm; margin-bottom: 1mm;\n  }",
    ".letter__text .subheading {\n    break-after: avoid;\n    page-break-after: avoid;\n    font-size: 11.5pt; color: #004080; font-weight: bold;\n    margin-top: 5mm; margin-bottom: 1.5mm;\n  }"
)

css = css.replace(
    ".letter__closing { border-top: 1pt solid #ccc; font-size: 10pt; line-height: 1.5;",
    ".letter__closing { border-top: 1pt solid #ccc; font-size: 10.5pt; line-height: 1.65;"
)

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated print CSS to v11")
