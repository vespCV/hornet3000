import os
import cv2
import torch
import numpy as np
from ultralytics import YOLOv10 as YOLO
import time
import subprocess

# Load the YOLOv10 model
model = YOLO('/home/detector/vespCV/last.pt')

# Define variables
image_capture_interval = 5  # Capture photo every 5 seconds
last_capture_time = time.time()  # Track the last capture time

# Path to save captured images (ensure crontab user has write permission)
image_folder = "/home/detector/vespCV/images"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)


def capture_image():
    # Capture an image with the CSI camera
    image_path = os.path.join(image_folder, "image.jpg")
    subprocess.run([
        "libcamera-still",
        "-o", image_path,  # Save the image
        "--width", "4656",
        "--height", "3496"
    ])
    return image_path


frame_count = 0

while True:
    # Check if it's time to capture a new image
    if time.time() - last_capture_time >= image_capture_interval:
        # Capture an image from the camera
        image_path = capture_image()

        # Load the full image (no magnification)
        img = cv2.imread(image_path)

        # Apply YOLOv10 object detection to the full image
        results = model(img)[0]

        # Check for class detection with high confidence
        conf = None

        for result in results.boxes.data.tolist():  # Each detection in format [x1, y1, x2, y2, conf, class]
            x1, y1, x2, y2, conf, cls = result[:6]
            if conf > 0.1:  # If confidence is above 0.1
                # Print the detected class and confidence
                print(f'Processed frame {frame_count}, class detected: {cls}, confidence: {conf}')

                # Save frame for every detection with a confidence above the threshold
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                save_path = os.path.join(image_folder, f"class_{int(cls)}_{conf}_{timestamp}.jpg")
                cv2.imwrite(save_path, img)  # Save the full image
                print(f"Saved image: {save_path}")

        # Update the time of the last capture
        last_capture_time = time.time()

        # Increase the frame count for each capture
        frame_count += 1

# This line won't be executed with crontab
print(f'Finished processing.')