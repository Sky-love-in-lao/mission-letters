import json
import datetime

index_file = 'letters/index.json'
with open(index_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

for l in data['letters']:
    if l['id'] == '2026-09':
        l['updatedAt'] = datetime.datetime.utcnow().isoformat() + 'Z'
        break

with open(index_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

