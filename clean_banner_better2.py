from PIL import Image

img = Image.open('assets/img/default-banner.png').convert('RGB')
w, h = img.size

# Let's crop from 340 to w
col = img.crop((950, 0, 951, h))
stretched = col.resize((1024 - 340, h))

out = img.copy()

# Paste with a soft mask to blend it with whatever is at 340 (maybe blue watercolor)
mask = Image.new('L', stretched.size, 255)
# make the first 20 pixels fade in
for x in range(20):
    for y in range(h):
        mask.putpixel((x, y), int(255 * (x/20.0)))

out.paste(stretched, (340, 0), mask)
out.save('assets/img/clean-banner.png')
print("Saved clean-banner.png with soft edge")
