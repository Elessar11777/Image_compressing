import os
from PIL import Image
import multiprocessing

# Set the directory path to search for BMP and PNG images
directory = "/path/to/directory"

def process_image(image_file):
    # Open the image file and convert it to a PIL Image object
    image = Image.open(image_file)

    # If the file ends with ".bmp", convert it to a PNG image and compress it
    if image_file.endswith(".bmp"):
        png_file = os.path.join(os.path.dirname(image_file), os.path.basename(image_file).replace(".bmp", ".png"))
        png_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
        png_image.paste(image, (0, 0), image.convert("RGBA"))
        png_image.save(png_file, optimize=True, compress_level=9)
        return png_file

    return None

def main():
    image_files = []

    # Recursively search for BMP and PNG images in the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".bmp") or file.endswith(".png"):
                image_files.append(os.path.join(root, file))
            else:
                # If the file is not BMP or PNG, delete it
                file_path = os.path.join(root, file)
                os.remove(file_path)

    # Process BMP and PNG files using multiprocessing with a pool of 8 workers
    cpu_count = 8
    with multiprocessing.Pool(cpu_count) as pool:
        processed_files = pool.map(process_image, image_files)

    # Remove the original image files
    for original_file, processed_file in zip(image_files, processed_files):
        if processed_file:
            os.remove(original_file)

if __name__ == '__main__':
    main()
