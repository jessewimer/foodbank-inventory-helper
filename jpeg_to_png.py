# from PIL import Image

# img = Image.open("assets/foodbank_logo.jpeg")
# img.save("assets/new_fb_logo.png", "PNG")


from PIL import Image
import numpy as np

# Open as RGBA
img = Image.open("assets/Database.png").convert("RGBA")
data = np.array(img)

# Split color and alpha
rgb = data[..., :3]
alpha = data[..., 3:4] / 255.0

# Premultiply RGB by alpha
rgb = (rgb * alpha).astype(np.uint8)

# Create solid black background image
black_bg = np.zeros_like(data)
black_bg[..., :3] = rgb
black_bg[..., 3] = 255  # Set alpha to fully opaque

# Convert back to image and save without transparency
final_img = Image.fromarray(black_bg[..., :3], mode="RGB")
final_img.save("your_icon2.ico", format="ICO", sizes=[
    (16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)
])