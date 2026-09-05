import re

with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. @page margin to 5mm (hides headers/footers automatically, puts border at the very edge)
css = re.sub(
    r'@page\s*\{[^}]*\}',
    '@page {\n  size: A4;\n  margin: 5mm;\n}',
    css
)

# 2. Increase horizontal padding of .letter slightly for safety
css = re.sub(
    r'padding:\s*0\s*6mm\s*!important;',
    'padding: 0 8mm !important;',
    css
)

# 3. Increase vertical padding slightly on blocks to ensure they push past the 3.5mm border
css = css.replace(
    ".letter__text p { padding: 1.5mm 0; margin: 0;",
    ".letter__text p { padding: 2.5mm 0; margin: 0;"
)
css = css.replace(
    ".letter__row {\n    display: flex;\n    gap: 3mm;\n    padding: 3mm 0;\n    margin: 0;",
    ".letter__row {\n    display: flex;\n    gap: 3mm;\n    padding: 4.5mm 0;\n    margin: 0;"
)
css = css.replace(
    ".letter__figure {\n    padding: 3mm 0;\n    margin: 0;",
    ".letter__figure {\n    padding: 4.5mm 0;\n    margin: 0;"
)
css = css.replace(
    ".letter__hero {\n    display: block;\n    padding-top: 5mm;",
    ".letter__hero {\n    display: block;\n    padding-top: 7mm;"
)

# Update body::before border width to 3.5mm to make it look nice and substantial on the edge
css = re.sub(
    r'border:\s*2\.5mm\s*solid;',
    'border: 3.5mm solid;',
    css
)

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated print CSS to v7")
