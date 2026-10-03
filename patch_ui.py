import sys

file_path = 'assets/js/views/write_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target_html = """            <button type="button" class="btn btn--sm" data-action="bold" data-i="${index}" style="font-weight: bold;">B 굵게</button>
            <select class="btn btn--sm" data-action="color" data-i="${index}" style="padding: 0 8px; font-weight: bold;">
              <option value="">A 색상</option>
              <option value="#c62828">빨강</option>
              <option value="#1565c0">파랑</option>
              <option value="#2e7d32">초록</option>
              <option value="#e65100">주황</option>
              <option value="#6a1b9a">보라</option>
            </select>"""

replacement_html = """            <button type="button" class="btn btn--sm" data-action="bold" data-i="${index}" style="font-weight: bold;">B 굵게</button>
            <button type="button" class="btn btn--sm" data-action="color" data-color="#c62828" data-i="${index}" style="color: #c62828; font-weight: bold;">빨강</button>
            <button type="button" class="btn btn--sm" data-action="color" data-color="#1565c0" data-i="${index}" style="color: #1565c0; font-weight: bold;">파랑</button>
            <button type="button" class="btn btn--sm" data-action="color" data-color="#2e7d32" data-i="${index}" style="color: #2e7d32; font-weight: bold;">초록</button>"""

target_js = """  $$('.block__format select[data-action=color]', wrap).forEach(select => {
    select.onchange = () => {
      const color = select.value;
      if (!color) return;
      
      const i = Number(select.dataset.i);
      const textarea = wrap.querySelector(`textarea[data-i="${i}"]`);"""

replacement_js = """  $$('.block__format button[data-action=color]', wrap).forEach(button => {
    button.onclick = () => {
      const color = button.dataset.color;
      if (!color) return;
      
      const i = Number(button.dataset.i);
      const textarea = wrap.querySelector(`textarea[data-i="${i}"]`);"""

target_js2 = """      persist(root);
      
      select.value = ""; // reset
      textarea.focus();"""

replacement_js2 = """      persist(root);
      
      textarea.focus();"""

code = code.replace(target_html, replacement_html)
code = code.replace(target_js, replacement_js)
code = code.replace(target_js2, replacement_js2)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("patched UI")
