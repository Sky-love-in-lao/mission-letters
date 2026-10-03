import json, os, sys, hashlib, base64, datetime
from PIL import Image, ImageDraw, ImageFont
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

if len(sys.argv) < 2:
    print("Usage: python3 publish.py <path_to_unencrypted_json>")
    sys.exit(1)

input_file = sys.argv[1]
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

letter_id = data['id']
period = data['body'].get('period', f"{letter_id} 편지")
password = data.get('password')

if not password:
    print("Error: No password found in JSON.")
    sys.exit(1)

print(f"Publishing {letter_id} ({period})...")

# 1. Generate OG Image
og_img_path = f"assets/img/og-{letter_id}.png"
canvas = Image.new('RGB', (1200, 630), "#fbf9f4")
banner = Image.open('assets/img/clean-banner.png')
family_crop = banner.crop((90, 0, 310, banner.height))

fade_w = 40
mask = Image.new("L", family_crop.size, 255)
for x in range(family_crop.width):
    alpha = 255
    if x < fade_w: alpha = int(255 * (x / fade_w))
    elif x > family_crop.width - fade_w: alpha = int(255 * ((family_crop.width - x) / fade_w))
    for y in range(family_crop.height): mask.putpixel((x, y), alpha)

scale = 2.5
new_w, new_h = int(family_crop.width * scale), int(family_crop.height * scale)
family_large = family_crop.resize((new_w, new_h), Image.Resampling.LANCZOS)
mask_large = mask.resize((new_w, new_h), Image.Resampling.LANCZOS)

canvas.paste(family_large, (100, (630 - new_h) // 2), mask_large)

draw = ImageDraw.Draw(canvas)
try:
    font_top = ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo.ttc", 65, index=0)
    font_bot = ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo.ttc", 85, index=0)
except:
    font_top = ImageFont.load_default()
    font_bot = ImageFont.load_default()

text_color = "#4b282d"
text_bot = "두손 모음 편지"

x_text, y_text = 650, 220
draw.text((x_text + 30, y_text), period, font=font_top, fill=text_color, stroke_width=2, stroke_fill=text_color)
draw.text((x_text, y_text + 90), text_bot, font=font_bot, fill=text_color, stroke_width=3, stroke_fill=text_color)

canvas.save(og_img_path)
print(f" -> Generated {og_img_path}")

# 2. Generate Redirect HTML
html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta property="og:title" content="라O스 ㅅ교편지 - 박OO, 김OO ㅅ교사">
  <meta property="og:description" content="{period} 두손 모음 편지와 ㄱ도제목">
  <meta property="og:image" content="https://sky-love-in-lao.github.io/mission-letters/{og_img_path}">
  <meta property="og:type" content="website">
  <meta http-equiv="refresh" content="0; url=index.html#/letter/{letter_id}">
  <title>{period} 편지</title>
</head>
<body>
  <p>편지로 이동 중입니다...</p>
  <script>window.location.replace("index.html#/letter/{letter_id}");</script>
</body>
</html>"""

html_path = f"{letter_id}.html"
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f" -> Generated {html_path}")

# 3. Encrypt JSON
body_str = json.dumps(data['body'], separators=(',', ':'), ensure_ascii=False).encode('utf-8')
salt = os.urandom(16)
iv = os.urandom(12)
kdf_iterations = 210000
key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, kdf_iterations, 32)
ciphertext = AESGCM(key).encrypt(iv, body_str, None)

encrypted_data = {
    'schemaVersion': 1,
    'id': letter_id,
    'publishedAt': data.get('publishedAt', datetime.datetime.utcnow().strftime('%Y-%m-%d')),
    'updatedAt': datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z'),
    'crypto': {
        'alg': 'AES-GCM', 'kdf': 'PBKDF2-SHA256', 'iterations': kdf_iterations,
        'salt': base64.b64encode(salt).decode('utf-8'), 'iv': base64.b64encode(iv).decode('utf-8')
    },
    'ciphertext': base64.b64encode(ciphertext).decode('utf-8')
}
if 'hint' in data: encrypted_data['hint'] = data['hint']

enc_path = f"letters/{letter_id}.json"
with open(enc_path, 'w', encoding='utf-8') as f:
    json.dump(encrypted_data, f, indent=2, ensure_ascii=False)
print(f" -> Encrypted to {enc_path}")

# 4. Update index.json
index_file = 'letters/index.json'
with open(index_file, 'r', encoding='utf-8') as f:
    idx_data = json.load(f)

# Remove existing if any
idx_data['letters'] = [l for l in idx_data['letters'] if l['id'] != letter_id]
idx_data['letters'].insert(0, {
  "id": letter_id,
  "publishedAt": encrypted_data['publishedAt'],
  "updatedAt": encrypted_data['updatedAt']
})

with open(index_file, 'w', encoding='utf-8') as f:
    json.dump(idx_data, f, indent=2)
print(" -> Updated letters/index.json")

print("\nDone! To deploy, run:")
print(f"git add {og_img_path} {html_path} {enc_path} {index_file}")
print(f"git commit -m 'Publish {letter_id}' && git push")
