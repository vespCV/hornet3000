import os
from PIL import Image

image_dir = '/Users/md/Developer/vespCV/data/images/val/'

for filename in os.listdir(image_dir):
    if filename.endswith('.jpg'):
        try:
            img_path = os.path.join(image_dir, filename)
            with Image.open(img_path) as img:
                img.verify()  # This will check for integrity
            print(f"{filename} is OK")
        except (IOError, SyntaxError) as e:
            print(f"Error with {filename}: {e}")
