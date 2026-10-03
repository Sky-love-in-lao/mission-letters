import sys, re

file_js = 'assets/js/store.js'
with open(file_js, 'r', encoding='utf-8') as f:
    code = f.read()

target = """  supportNote: 'ㄱ도와 후원 감사합니다.',
  supportBank: '국민은행',
  supportAccount: '410190-85-890840 (박종진 선교사 가상계좌)',
  supportHolder: '(재)기독교대한성결교회'"""

new_defaults = """  supportNote: '첫 송금시 ㅅ교국(02-3459-1031~4)으로 전화 후 박OO/김OO ㅅ교사 후원임을 꼭 알려주세요!\\n\\n※라O스는 보안이 필요한 ㅅ교지이므로, 보안처리를합니다. 이 편지는 개인 ㄱ도와 게시용으로 열람해 주시고 인터넷(SNS,블로그 등) 공유는 삼가주시기 부탁드립니다.',
  supportBank: '국민은행',
  supportAccount: '410190-85-890840 (박O진 ㅅ교사 가상계좌)',
  supportHolder: '(재)기독교대한성결ㄱ회'"""

if target in code:
    code = code.replace(target, new_defaults)
else:
    print("Could not find target in store.js")

with open(file_js, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V42 Store: Updated default support info")
