import json

file_json = '/Users/user/Downloads/letter-2026-09 (2).json'
with open(file_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

s = data['body']['support']

s['note'] = '첫 송금시 ㅅ교국(02-3459-1031~4)으로 전화 후 박OO/김OO ㅅ교사 후원임을 꼭 알려주세요!\n\n※라O스는 보안이 필요한 ㅅ교지이므로, 보안처리를합니다. 이 편지는 개인 ㄱ도와 게시용으로 열람해 주시고 인터넷(SNS,블로그 등) 공유는 삼가주시기 부탁드립니다.'
s['bank'] = '국민은행'
s['account'] = '410190-85-890840 (박O진 ㅅ교사 가상계좌)'
s['holder'] = '(재)기독교대한성결ㄱ회'

with open(file_json, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated letter JSON in Downloads!")
