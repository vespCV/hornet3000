# Input: 16MP Sony IMX519 ArduCam CSI
# Output: 1280x720 image in folder images (makes the folder if it doesn't exist)

import subprocess
import os

def capture_image():
    # Create the 'images' folder if it doesn't exist
    os.makedirs("/home/detector/vespCV/images", exist_ok=True)
    
    # Capture an image in 1280x720 resolution and save it in the 'images' folder
    subprocess.run([
        "libcamera-still", 
        "-o", "/home/detector/vespCV/images/image.jpg",  # Save the image in the 'images' folder
        "--nopreview", 
        "--width", "1280", 
        "--height", "720"
    ])

if __name__ == "__main__":
    capture_image()
    print("Image captured and saved as images/image.jpg in 1280x720 resolution")
