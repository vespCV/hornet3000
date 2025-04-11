"""
This script validates the integrity of all JPG images in a specified directory.
It checks each image file to ensure it's not corrupted and can be properly opened.

Functionality:
- Scans a directory for JPG files
- Attempts to open and verify each image
- Prints status messages for each file:
  * "filename is OK" for valid images
  * Error message for corrupted or invalid images

Usage:
Simply replace 'path_to_folder' and run the script and it will process all JPG files in the specified image_dir.
"""
import os
from PIL import Image

image_dir = 'path_to_folder'

for filename in os.listdir(image_dir):
    if filename.endswith('.jpg'):
        try:
            img_path = os.path.join(image_dir, filename)
            with Image.open(img_path) as img:
                img.verify()  # This will check for integrity
            print(f"{filename} is OK")
        except (IOError, SyntaxError) as e:
            print(f"Error with {filename}: {e}")
