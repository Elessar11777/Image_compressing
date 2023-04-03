import os
from PIL import Image

# Set the directory path to search for BMP and PNG images
directory = "/path/to/directory"

# Recursively search for BMP and PNG images in the directory and its subdirectories
for root, dirs, files in os.walk(directory):
    for file in files:
        if not file.endswith(".bmp") and not file.endswith(".png"):
            # If the file is not BMP or PNG, delete it
            file_path = os.path.join(root, file)
            os.remove(file_path)
        else:
            # Process BMP and PNG files
            image_file = os.path.join(root, file)

            # Open the image file and convert it to a PIL Image object
            image = Image.open(image_file)

            # If the file ends with ".bmp", convert it to a PNG image and compress it
            if file.endswith(".bmp"):
                png_file = os.path.join(root, file.replace(".bmp", ".png"))
                png_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
                png_image.paste(image, (0, 0), image.convert("RGBA"))
                png_image.save(png_file, optimize=True, compress_level=9)

            # Remove the original image file
            os.remove(image_file)