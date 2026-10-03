import json
import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import datetime

letter_path = 'letters/2026-09.json'
with open(letter_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# If it's already encrypted, skip
if 'ciphertext' in data:
    print("Already encrypted!")
    sys.exit(0)

password = data.get('password')
if not password:
    print("No password found!")
    sys.exit(1)

body_str = json.dumps(data['body'], separators=(',', ':'), ensure_ascii=False).encode('utf-8')

salt = get_random_bytes(16)
iv = get_random_bytes(12)
kdf_iterations = 210000

key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, kdf_iterations, 32)

cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
ciphertext, tag = cipher.encrypt_and_digest(body_str)

full_ciphertext = ciphertext + tag

encrypted_data = {
    'schemaVersion': 1,
    'id': data['id'],
    'publishedAt': data.get('publishedAt', '2026-09-01'),
    'updatedAt': datetime.datetime.utcnow().isoformat() + 'Z',
    'crypto': {
        'alg': 'AES-GCM',
        'kdf': 'PBKDF2-SHA256',
        'iterations': kdf_iterations,
        'salt': base64.b64encode(salt).decode('utf-8'),
        'iv': base64.b64encode(iv).decode('utf-8')
    },
    'ciphertext': base64.b64encode(full_ciphertext).decode('utf-8')
}
if 'hint' in data:
    encrypted_data['hint'] = data['hint']

with open(letter_path, 'w', encoding='utf-8') as f:
    json.dump(encrypted_data, f, indent=2, ensure_ascii=False)

print("Encrypted successfully!")
