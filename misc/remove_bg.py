from rembg import remove
from PIL import Image
import io

# Load your image
with open("foodbank_logo1.png", "rb") as input_file:
    input_data = input_file.read()

# Remove background
output_data = remove(input_data)

# Save the output
with open("foodbank_logo1_no_bg.png", "wb") as output_file:
    output_file.write(output_data)
