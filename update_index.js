const fs = require('fs');

const indexFile = 'letters/index.json';
const indexData = JSON.parse(fs.readFileSync(indexFile, 'utf8'));

// Find 2026-09
const letter = indexData.letters.find(l => l.id === '2026-09');
if (letter) {
  letter.updatedAt = new Date().toISOString();
} else {
  indexData.letters.push({
    id: '2026-09',
    publishedAt: '2026-09-01',
    updatedAt: new Date().toISOString()
  });
}

fs.writeFileSync(indexFile, JSON.stringify(indexData, null, 2) + '\n');
console.log('Updated index.json');
