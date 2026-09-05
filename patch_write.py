with open('assets/js/views/write_v2.js', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    "document.body.appendChild(temp);\n      loadLetterImages(temp);",
    "document.body.appendChild(temp);\n      const app = document.getElementById('app');\n      if(app) app.style.display = 'none';\n      loadLetterImages(temp);"
)
code = code.replace(
    "temp.remove();",
    "temp.remove();\n      if(app) app.style.display = '';"
)

with open('assets/js/views/write_v2.js', 'w', encoding='utf-8') as f:
    f.write(code)
