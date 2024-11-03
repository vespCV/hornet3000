# Input: USB camera still image every 5 sec
# Output: image in folder image names vvn_timestamp
# Goal: prototype for Asian hornet detector

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

# Path to save captured images
image_folder = "/home/detector/vespCV/images"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

def capture_image():
    # Capture an image with the CSI camera
    image_path = os.path.join(image_folder, "image.jpg")
    subprocess.run([
        "libcamera-still", 
        "-o", image_path,  # Save the image
        "--width", "1280", 
        "--height", "720"
    ])
    return image_path

frame_count = 0
while True:
    # Check if it's time to capture a new image
    if time.time() - last_capture_time >= image_capture_interval:
        # Capture an image from the camera
        image_path = capture_image()

        # Load the captured image
        frame = cv2.imread(image_path)

        # Apply YOLOv10 object detection to the captured image
        results = model(frame)[0]

        # Check for class 0 detection with high confidence
        class_0_now_detected = False  # Reset class detection for each image
        for result in results.boxes.data.tolist():  # Each detection in format [x1, y1, x2, y2, conf, class]
            x1, y1, x2, y2, conf, cls = result[:6]
            if cls == 0 and conf > 0.7:  # If class 0 is detected
                class_0_now_detected = True

                # Save frame if confidence crosses the threshold (above 0.77)
                if conf >= 0.77:
                    # Save frame as JPG with timestamp in the "images" folder
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    save_path = os.path.join(image_folder, f"VVN_{timestamp}.jpg")
                    cv2.imwrite(save_path, frame)
                    print(f"Saved image: {save_path}")
        
        # Print a message for each frame processed, even if no class 0 was detected
        frame_count += 1
        print(f'Processed frame {frame_count}, class 0 detected: {class_0_now_detected}')

        # Update the time of the last capture
        last_capture_time = time.time()

    # Wait for 1 ms and check if 'q' is pressed to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print(f'Finished processing.')
