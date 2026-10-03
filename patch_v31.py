import sys, re

file_path = 'assets/css/app.css'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Make the prayer box in the web view clearly readable
target = """.prayers__text { 
  display: block;
  font-size: 17px; 
  line-height: 1.85; 
  color: var(--ink-soft);
  margin-top: 12px;
}"""

new = """.prayers__subtitle {
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

code = code.replace(target, new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V31 CSS patches")
