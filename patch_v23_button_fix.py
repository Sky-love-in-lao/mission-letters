import sys

file_path = 'assets/js/views/write_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = """        backBtn.onclick = () => {
            window.location.reload(); // Quickest way to restore state!
        };"""
new = """        backBtn.onclick = () => {
            root.innerHTML = '';
            root.style.display = 'none';
            document.body.style.background = '';
            document.body.style.padding = '';
            document.getElementById('nav').style.display = '';
            document.getElementById('app').style.display = '';
            backBtn.remove();
        };
        document.getElementById('app').style.display = 'none';"""

code = code.replace(target, new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed back button behavior")
