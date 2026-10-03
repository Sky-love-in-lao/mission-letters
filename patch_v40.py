import sys, re

# 1. Update letter.js
file_js = 'assets/js/views/letter.js'
with open(file_js, 'r', encoding='utf-8') as f:
    code = f.read()

target_html = """        <p class="lock__desc">비밀번호를 입력하면 편지를 읽을 수 있습니다.</p>
        <form class="lock__form" id="lock-form">
          <input type="password" id="pw" placeholder="비밀번호" autocomplete="off"
                 autocapitalize="none" spellcheck="false" enterkeyhint="go" aria-label="비밀번호">
          <button type="submit" class="btn btn--primary btn--lg">편지 열기</button>
        </form>
        ${meta.hint ? `<p class="lock__hint">힌트: ${esc(meta.hint)}</p>` : ''}"""

new_html = """        <p class="lock__desc">비밀번호를 입력하면 편지를 읽을 수 있습니다.</p>
        ${meta.hint ? `<p class="lock__hint">힌트: ${esc(meta.hint)}</p>` : ''}
        <form class="lock__form" id="lock-form">
          <input type="password" id="pw" placeholder="비밀번호" autocomplete="off"
                 autocapitalize="none" spellcheck="false" enterkeyhint="go" aria-label="비밀번호">
          <button type="submit" class="btn btn--primary btn--lg">편지 열기</button>
        </form>"""

code = code.replace(target_html, new_html)

with open(file_js, 'w', encoding='utf-8') as f:
    f.write(code)

# 2. Update app.css
file_css = 'assets/css/app.css'
with open(file_css, 'r', encoding='utf-8') as f:
    code = f.read()

# lock__title
target_title = ".lock__title { font-family: var(--serif); font-size: clamp(26px, 3.6vw, 32px); font-weight: 700; color: var(--accent); margin: 0 0 10px; line-height: 1.4; }"
new_title = ".lock__title { font-family: var(--serif); font-size: clamp(22px, 3.2vw, 26px); font-weight: 700; color: var(--accent); margin: 0 0 10px; line-height: 1.4; }"
code = code.replace(target_title, new_title)

# lock__desc (change margin-bottom from 28px to 8px)
target_desc = ".lock__desc { font-size: 18px; color: #2563eb; font-weight: 600; margin: 0 0 28px; line-height: 1.75; }"
new_desc = ".lock__desc { font-size: 18px; color: #2563eb; font-weight: 600; margin: 0 0 8px; line-height: 1.75; }"
code = code.replace(target_desc, new_desc)

# lock__hint (remove animation, change margin)
target_hint = """.lock__hint { 
  font-size: 18px; 
  color: #dc2626; 
  font-weight: bold;
  margin: 18px 0 0; 
  animation: hint-blink 1.2s infinite;
}"""
new_hint = """.lock__hint { 
  font-size: 18px; 
  color: #dc2626; 
  font-weight: bold;
  margin: 0 0 28px; 
}"""
code = code.replace(target_hint, new_hint)

# remove keyframes
target_keyframes = """@keyframes hint-blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.2; }
}"""
code = code.replace(target_keyframes, "")

with open(file_css, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V40: Moved hint, stopped blinking, reduced title size")
