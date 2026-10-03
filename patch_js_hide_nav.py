import sys, re

file_path = 'assets/js/views/write_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = """      const app = document.getElementById('app');
      if(app) app.style.display = 'none';"""

new_code = """      const app = document.getElementById('app');
      const nav = document.getElementById('nav');
      const toast = document.getElementById('toast');
      if(app) app.style.display = 'none';
      if(nav) nav.style.display = 'none';
      if(toast) toast.style.display = 'none';"""

code = code.replace(target, new_code)

target_restore = """      if(app) app.style.display = '';"""

new_restore = """      if(app) app.style.display = '';
      if(nav) nav.style.display = '';
      if(toast) toast.style.display = '';"""

code = code.replace(target_restore, new_restore)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Added explicit JS hiding for nav and toast during print")
