from PIL import Image

img = Image.open('assets/img/default-banner.png').convert('RGB')
w, h = img.size

col = img.crop((950, 0, 951, h))
stretched = col.resize((1024 - 360, h))
out2 = img.copy()
out2.paste(stretched, (360, 0))

out2.save('assets/img/clean-banner.png')
print("Saved clean-banner.png (stretched column)")
