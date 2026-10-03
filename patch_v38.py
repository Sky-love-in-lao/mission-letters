import sys, re

file_path = 'assets/css/app.css'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = ".lock__hint { font-size: 14px; color: var(--ink-faint); margin: 18px 0 0; }"
new_rule = """.lock__hint { 
  font-size: 18px; 
  color: #dc2626; 
  font-weight: bold;
  margin: 18px 0 0; 
  animation: hint-blink 1.2s infinite;
}
@keyframes hint-blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.2; }
}"""

if target in code:
    code = code.replace(target, new_rule)
else:
    print("Could not find the target CSS rule.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V38: Made hint red, larger, and blinking")
