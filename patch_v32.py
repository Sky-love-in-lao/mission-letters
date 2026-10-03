import sys, re

# 1. Update app.css for inline subtitle and larger fonts
file_css = 'assets/css/app.css'
with open(file_css, 'r', encoding='utf-8') as f:
    css = f.read()

target_css = """.prayers__subtitle {
  font-size: 20px;
  font-weight: 700;
  display: block;
  margin-bottom: 4px;
}
.prayers__text { 
  display: block;
  font-size: 18px; 
  line-height: 1.7; 
  color: var(--ink-soft);
  margin-top: 8px;
  margin-bottom: 24px;
}"""

new_css = """.prayers__subtitle {
  font-size: 22px;
  font-weight: 700;
  display: inline;
}
.prayers__text { 
  display: block;
  font-size: 20px; 
  line-height: 1.7; 
  color: var(--ink-soft);
  margin-top: 8px;
  margin-bottom: 28px;
}"""

css = css.replace(target_css, new_css)
with open(file_css, 'w', encoding='utf-8') as f:
    f.write(css)

# 2. Update render_v2.js to add emojis to web view (AND PDF if it's the same HTML!)
file_js = 'assets/js/render_v2.js'
with open(file_js, 'r', encoding='utf-8') as f:
    js = f.read()

# Add emoji to Prayer Box
target_prayer_html = """<h2 class="prayers__title">ㄱ도해 주세요!</h2>"""
new_prayer_html = """<h2 class="prayers__title">🙏 ㄱ도해 주세요!</h2>"""
js = js.replace(target_prayer_html, new_prayer_html)

# Add emoji to Support Box
target_support_html = """<h2 class="support__title">사역에 동참하기</h2>"""
new_support_html = """<h2 class="support__title">💌 사역에 동참하기</h2>"""
js = js.replace(target_support_html, new_support_html)

with open(file_js, 'w', encoding='utf-8') as f:
    f.write(js)

print("Applied V32 patches for emojis and inline subtitle")
