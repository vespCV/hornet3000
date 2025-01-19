# Input: 16MP sony IMX519 ArduCam camera still image every 5 sec
# Output: image in folder image names vvn_timestamp
# Goal: prototype for Asian hornet detector

import os
import cv2
import torch
import numpy as np
from ultralytics import YOLOv10 as YOLO
import time
import subprocess
import RPi.GPIO as GPIO

# Load the YOLOv10 model
model = YOLO('/home/detector/vespCV/last.pt')

# Define variables
image_capture_interval = 5  # Capture photo every 5 seconds
last_capture_time = time.time()  # Track the last capture time
last_detection_time = 0  # Track the last detection time for LED control

# Path to save captured images
image_folder = "/home/detector/vespCV/images"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED_PIN = 21
GPIO.setup(LED_PIN, GPIO.OUT)

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
        class_0_now_detected = False
        max_confidence = 0
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, conf, cls = result[:6]
            if cls == 0 and conf > 0.7:
                class_0_now_detected = True
                max_confidence = max(max_confidence, conf)

        # Handle LED and image saving logic
        if class_0_now_detected:
            # Save frame if confidence crosses the threshold
            if max_confidence >= 0.77:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                save_path = os.path.join(image_folder, f"VVN_{timestamp}.jpg")
                cv2.imwrite(save_path, frame)
                print(f"Saved image: {save_path}")
            
            # Turn on LED only if not already on from a recent detection
            current_time = time.time()
            if current_time - last_detection_time > 10:
                print("LED on")
                GPIO.output(LED_PIN, GPIO.HIGH)
                last_detection_time = current_time
        
        # Check if LED needs to be turned off after 10 seconds
        if GPIO.input(LED_PIN) == GPIO.HIGH and time.time() - last_detection_time >= 10:
            print("LED off")
            GPIO.output(LED_PIN, GPIO.LOW)
        
        # Print a message for each frame processed
        frame_count += 1
        print(f'Processed frame {frame_count}, class 0 detected: {class_0_now_detected}')

        # Update the time of the last capture
        last_capture_time = time.time()

    # Wait for 1000 ms and check if 'q' is pressed to exit
    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break

# Cleanup GPIO
GPIO.cleanup()

print(f'Finished processing.')
