import os
import zipfile
from io import BytesIO
from PIL import Image

# Set the path to the zip archive containing BMP and PNG images
zip_file_path = "08_02_2023.zip"

# Open the zip archive and loop over its contents
with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
    num_files_processed = 0
    with zipfile.ZipFile("08_02_2023_c.zip", mode="w") as new_zip:
        for zip_info in zip_file.infolist():
            if not zip_info.filename.endswith(".bmp") and not zip_info.filename.endswith(".png"):
                # If the file is not BMP or PNG, skip it
                continue

            # Open the file as a binary stream
            with zip_file.open(zip_info, 'r') as file:
                # Read the file contents into memory
                file_contents = BytesIO(file.read())

                # Open the image file and convert it to a PIL Image object
                image = Image.open(file_contents)

                # If the file ends with ".bmp", convert it to a PNG image and compress it
                if zip_info.filename.endswith(".bmp"):
                    png_file_name = zip_info.filename.replace(".bmp", ".png")

                    png_file_contents = BytesIO()
                    png_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
                    png_image.paste(image, (0, 0), image.convert("RGBA"))
                    png_image.save(png_file_contents, format="PNG", optimize=True, compress_level=9)
                    png_file_contents.seek(0)
                    new_zip.writestr(png_file_name, png_file_contents.read())

                else:
                    new_zip.writestr(zip_info, file_contents.read())

                # Increment the number of files processed and print a progress message
                num_files_processed += 1
                print(f"Processed file {num_files_processed}: {zip_info.filename}")

    # Replace the original zip archive with the new one
    os.remove(zip_file_path)
    os.rename("new_archive.zip", zip_file_path)

    print("Finished processing all BMP and PNG files in the zip archive.")
