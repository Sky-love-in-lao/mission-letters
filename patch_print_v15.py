import re

with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Remove column-count from .letter
css = css.replace(
    "column-count: 2;\n    column-gap: 8mm;",
    ""
)

# 2. Add .letter__sheet with column-count
sheet_css = """
  .letter__sheet {
    column-count: 2;
    column-gap: 8mm;
  }
"""
css = css.replace(".support { display: none !important; }", sheet_css + "\n  .support { display: none !important; }")

# 3. Ensure .letter__hero is pushed down
css = css.replace(
    "padding-top: 12mm; /* Push hero well down from top border */",
    "padding-top: 12mm; margin-top: 4mm; /* Push hero well down from top border */"
)

# Also ensure .letter__head (if hero is not used) is pushed down
head_css = """
  .letter__head {
    padding-top: 12mm;
    margin-top: 4mm;
    margin-bottom: 8mm;
  }
"""
css = css.replace(".support { display: none !important; }", head_css + "\n  .support { display: none !important; }")

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated print CSS to v15")
