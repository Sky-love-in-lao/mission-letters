import sys, re

file_css = 'assets/css/app.css'
with open(file_css, 'r', encoding='utf-8') as f:
    code = f.read()

# Remove the display: none!
target = """.letter__hero--banner .letter__hero-text {
  display: none !important;
}"""

# We want the text to appear nicely on the right side.
new_css = """.letter__hero--banner .letter__hero-text {
  /* display: none !important; */
  position: absolute;
  top: 0; right: 0; bottom: 0; left: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-end; /* right align */
  padding-right: 8%; /* some spacing from the right */
  text-align: right;
}
.letter__hero--banner .letter__title {
  font-size: clamp(24px, 4vw, 36px);
  color: #4b282d !important; /* The dark brown color from their text */
  font-weight: 800;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(255,255,255,0.8);
}
"""

if target in code:
    code = code.replace(target, new_css)
else:
    print("Could not find target in CSS")

with open(file_css, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V42 CSS: Enabled dynamic text on banner")
