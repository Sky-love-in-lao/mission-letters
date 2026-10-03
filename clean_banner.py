from PIL import Image

img = Image.open('assets/img/default-banner.png').convert('RGB')
w, h = img.size

# We will use the clean peach background from x=900 to x=1000
patch = img.crop((900, 0, 1000, h))

# The text is from x=380 to x=900
# We will tile the patch over the text area
# Let's fade it in from x=450 so we don't overwrite the family and the blue-to-peach transition.
# Wait, the transition is around x=300 to x=400.
# The text starts at x=400. Let's just paste the patch starting from x=430 to x=900

out = img.copy()
for x in range(430, 950, 100):
    # To avoid sharp edges, we can flip the patch left-right on alternating tiles
    p = patch if (x//100)%2 == 0 else patch.transpose(Image.FLIP_LEFT_RIGHT)
    # Paste using a soft mask? No, just pasting might have visible seams.
    out.paste(p, (x, 0))

# Let's save it
out.save('assets/img/clean-banner.png')
print("Saved clean-banner.png")
