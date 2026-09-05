with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    css = f.read()

new_rules = """
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
"""

# replace .letter__photo rule with the new row rules and photo rule
css = css.replace(
    ".letter__photo { max-height: 80mm; width: 100%; object-fit: contain; }",
    new_rules.strip()
)

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(css)
