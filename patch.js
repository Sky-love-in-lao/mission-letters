const fs = require('fs');

// 1. render.js 수정
let renderStr = fs.readFileSync('assets/js/render.js', 'utf8');
renderStr = renderStr.replace(
  "if (block.type === 'image' && block.driveId) {",
  "if (block.type === 'image' && (block.driveId || block.image)) {"
);
renderStr = renderStr.replace(
  "&& rest[i].type === 'image' && rest[i].driveId",
  "&& rest[i].type === 'image' && (rest[i].driveId || rest[i].image)"
);
renderStr = renderStr.replace(
  /function figureHTML\(block, className\) {[\s\S]*?return `<figure class="\${className}">[\s\S]*?<\/figure>`;\n}/,
  `function figureHTML(block, className) {
  const imgSrc = block.image ? \`<img src="\${esc(block.image)}" class="letter__photo" alt="">\` : 
                 \`<img class="letter__photo" data-drive-id="\${esc(block.driveId)}" alt="" referrerpolicy="no-referrer">\`;
  const href = block.image ? esc(block.image) : esc(driveViewUrl(block.driveId));
  return \`<figure class="\${className}">
      <a href="\${href}" target="_blank" rel="noopener noreferrer">
        \${imgSrc}
      </a>
      \${block.caption ? \`<figcaption>\${esc(block.caption)}</figcaption>\` : ''}
    </figure>\`;
}`
);
fs.writeFileSync('assets/js/render.js', renderStr, 'utf8');

// 2. write.js 수정
let writeStr = fs.readFileSync('assets/js/views/write.js', 'utf8');
writeStr = writeStr.replace(
  /<img data-drive-id="\${esc\(block\.driveId \|\| ''\)}" alt="" referrerpolicy="no-referrer">/,
  `\${block.image ? \`<img src="\${esc(block.image)}" alt="">\` : \`<img data-drive-id="\${esc(block.driveId || '')}" alt="" referrerpolicy="no-referrer">\`}`
);
writeStr = writeStr.replace(
  /if \(!img\.dataset\.driveId\) return;/,
  `if (!img.dataset.driveId) return;` // leave as is, since block.image images don't need async loading
);
fs.writeFileSync('assets/js/views/write.js', writeStr, 'utf8');

