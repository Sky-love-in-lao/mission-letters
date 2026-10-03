from PIL import Image
import numpy as np

# Open the original banner
img = Image.open('assets/img/default-banner.png').convert('RGB')
arr = np.array(img)

# The image is 1122x158 (or something). Let's check dimensions.
h, w, c = arr.shape

# The text "2026년 9월 두손 모음 편지" is roughly in the middle-right.
# Let's sample a clean column from the far right (but before the edge fade if any)
# Let's look at x = w - 50
clean_column = arr[:, w-50:w-49, :].copy()

# The text seems to start around x=400 and ends around x=900
# I will just overwrite the whole text area with the clean peach background.
# Wait, stretching a single column might look artificial.
# Let's see if there's a clean patch of peach background.
