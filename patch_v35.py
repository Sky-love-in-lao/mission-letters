import sys, re

# 1. list.js
file_list = 'assets/js/views/list.js'
with open(file_list, 'r', encoding='utf-8') as f:
    code = f.read()

# revealTitles uses preferApi: true, change it to false
code = code.replace("{ preferApi: true }", "{ preferApi: false }")
with open(file_list, 'w', encoding='utf-8') as f:
    f.write(code)

# 2. write_v2.js
file_write = 'assets/js/views/write_v2.js'
with open(file_write, 'r', encoding='utf-8') as f:
    code = f.read()

# renderWrite uses preferApi: true, change it to false
code = code.replace("{ preferApi: true }", "{ preferApi: false }")
with open(file_write, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V35: Removed preferApi: true to avoid GitHub API rate limits")
