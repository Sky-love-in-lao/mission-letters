import re

with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace @page { ... } completely
css = re.sub(
    r'@page\s*\{[^}]*\}',
    '@page {\n  size: A4;\n  margin: 10mm 8mm;\n}',
    css
)

# Update body::before to draw exactly at the margin bounds
css = re.sub(
    r'top:\s*-8mm;\s*bottom:\s*-8mm;\s*left:\s*-8mm;\s*right:\s*-8mm;',
    'top: 0; bottom: 0; left: 0; right: 0;',
    css
)

# Update .letter padding to add horizontal inset, and avoid touching sides
css = re.sub(
    r'padding:\s*0\s*!important;',
    'padding: 2mm 6mm !important;',
    css
)

# Add top margin to hero so it doesn't touch the top border tightly
css = css.replace(
    ".letter__hero {\n    display: block;",
    ".letter__hero {\n    display: block;\n    margin-top: 4mm;"
)

# Fix Chrome column bug with translateZ
css = css.replace(
    "column-gap: 8mm;\n  }",
    "column-gap: 8mm;\n    transform: translateZ(0);\n  }"
)

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated print CSS to v5")
