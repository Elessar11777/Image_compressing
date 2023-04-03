from PIL import Image

# Open the BMP image file and convert it to PIL Image object
bmp_image = Image.open("1.bmp")

# Convert the image to PNG format and compress it
png_image = Image.new("RGBA", bmp_image.size, (255, 255, 255, 0))
png_image.paste(bmp_image, (0, 0), bmp_image.convert("RGBA"))
png_image.save("compressed_image.png", optimize=True, compress_level=9)