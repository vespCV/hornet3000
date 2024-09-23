# Input: test USB camera
# Output: capture photo every 5 seconds and save it to images if a VVN is detected
# Goal: simulate functions on RPI
# Note: q only works when not switching to other applications

import os
import cv2
import torch
import numpy as np
from ultralytics import YOLOv10 as YOLO
import time

# Load the YOLOv10 model
model = YOLO('content_data3000_24-09-20/content/runs/detect/train/weights/last.pt')

# Open the camera using libcamera
camera_index = 0  # Change if needed based on your setup
video_capture = cv2.VideoCapture(camera_index)

# Check if the camera opened successfully
if not video_capture.isOpened():
    print("Error: Could not open camera.")
    exit()

# Get camera properties
frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define variables
image_capture_interval = 5  # Capture photo every 5 seconds
last_capture_time = time.time()  # Track the last capture time

# Create the "images" folder if it doesn't exist
image_folder = "images"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# Show a blank window initially
cv2.imshow('Camera Feed', np.zeros((100, 100, 3), dtype=np.uint8))

frame_count = 0
while True:
    # Check if it's time to capture a new image
    if time.time() - last_capture_time >= image_capture_interval:
        ret, frame = video_capture.read()  # Capture a single frame
        if not ret:
            break

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
                    image_name = f"VVN_{timestamp}.jpg"
                    image_path = os.path.join(image_folder, image_name)
                    cv2.imwrite(image_path, frame)
                    print(f"Saved image: {image_path}")

        frame_count += 1
        print(f'Processed frame {frame_count}')

        # Resize the frame to 25% of its original size for display
        resized_frame = cv2.resize(frame, (int(frame_width * 0.25), int(frame_height * 0.25)))

        # Display the resized frame
        cv2.imshow('Camera Feed', resized_frame)

        # Update the time of the last capture
        last_capture_time = time.time()

    # Wait for 1 ms and check if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()

print(f'Finished processing.')
