import re

with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace @page { margin: 0; } with @page { margin: 16mm 15mm; }
css = re.sub(
    r'@page\s*\{\s*size:\s*A4;\s*margin:\s*0;\s*\}',
    '@page {\n  size: A4;\n  margin: 16mm 15mm;\n}',
    css
)

# Update body::before to use negative positioning to draw outside the page margin
# Old: top: 8mm; bottom: 8mm; left: 8mm; right: 8mm;
# New: top: -8mm; bottom: -8mm; left: -8mm; right: -8mm;
css = re.sub(
    r'top: 8mm;\s*bottom: 8mm;\s*left: 8mm;\s*right: 8mm;',
    'top: -8mm; bottom: -8mm; left: -8mm; right: -8mm;',
    css
)

# Remove padding from .letter since @page margin provides the spacing
css = re.sub(
    r'padding:\s*16mm\s*15mm\s*!important;',
    'padding: 0 !important;',
    css
)

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated print CSS to v4")
