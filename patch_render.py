with open('assets/js/render_v2.js', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('function plainHeadHTML(body) {', 'function plainHeadHTML(body, period) {')
code = code.replace('plainHeadHTML(body)', 'plainHeadHTML(body, period)')
code = code.replace('<h1 class="letter__title">', '${period ? `<div class="letter__period print-only">${esc(period)}</div>` : \'\'}\n      <h1 class="letter__title">')

with open('assets/js/render_v2.js', 'w', encoding='utf-8') as f:
    f.write(code)
