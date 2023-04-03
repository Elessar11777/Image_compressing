import os
import zipfile
from io import BytesIO
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# Set the path to the zip archive containing BMP and PNG images
zip_file_path = "08_02_2023.zip"

# Function to process a single file
def process_file(zip_info, zip_file):
    with zip_file.open(zip_info, 'r') as file:
        file_contents = BytesIO(file.read())
        image = Image.open(file_contents)

        if zip_info.filename.endswith(".bmp"):
            png_file_name = zip_info.filename.replace(".bmp", ".png")
            png_file_contents = BytesIO()
            png_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
            png_image.paste(image, (0, 0), image.convert("RGBA"))
            png_image.save(png_file_contents, format="PNG", optimize=True, compress_level=9)
            png_file_contents.seek(0)
            return (png_file_name, png_file_contents.read())
        else:
            return (zip_info, file_contents.read())

# Open the zip archive and loop over its contents
with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
    num_files_processed = 0
    with zipfile.ZipFile("new_archive.zip", mode="w") as new_zip:
        image_files = [zi for zi in zip_file.infolist() if zi.filename.endswith(".bmp") or zi.filename.endswith(".png")]

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda zi: process_file(zi, zip_file), image_files))

        for result in results:
            new_zip.writestr(result[0], result[1])
            num_files_processed += 1
            print(f"Processed file {num_files_processed}: {result[0].filename}")

# Replace the original zip archive with the new one
os.remove(zip_file_path)
os.rename("new_archive.zip", zip_file_path)

print("Finished processing all BMP and PNG files in the zip archive.")