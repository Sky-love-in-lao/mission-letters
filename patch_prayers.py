import sys

file_path = 'assets/css/app.css'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = """.prayers__item {
  counter-increment: prayer;
  display: grid;
  grid-template-columns: 56px 1fr;
  padding: 28px 0;
  border-top: 1px solid var(--line);
}
.prayers__item:last-child { border-bottom: 1px solid var(--line); }
.prayers__item > * { grid-column: 2; }
.prayers__item::before {
  content: counter(prayer, decimal-leading-zero);
  grid-column: 1; grid-row: 1;
  font-family: var(--serif);
  font-size: 20px;
  color: var(--ink-soft);
  line-height: 1.7;
}
.prayers__name { font-family: var(--serif); font-size: 21px; font-weight: 600; color: #cc0000; margin: 0 0 8px; line-height: 1.5; }
.prayers__text { font-size: 17px; line-height: 1.85; color: var(--ink-soft); }"""

replacement = """.prayers__item {
  counter-increment: prayer;
  display: block;
  padding: 24px 0;
  border-top: 1px solid var(--line);
}
.prayers__item:last-child { border-bottom: 1px solid var(--line); }
.prayers__item::before {
  content: counter(prayer, decimal-leading-zero) ". ";
  font-family: var(--serif);
  font-size: 21px;
  color: #cc0000;
  font-weight: 600;
  margin-right: 6px;
  display: inline;
}
.prayers__name { 
  display: inline;
  font-family: var(--serif); 
  font-size: 21px; 
  font-weight: 600; 
  color: #cc0000; 
  margin: 0; 
  line-height: 1.5; 
}
.prayers__text { 
  display: block;
  font-size: 17px; 
  line-height: 1.85; 
  color: var(--ink-soft);
  margin-top: 12px;
}"""

if target in code:
    code = code.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("patched prayers")
else:
    print("target not found")
