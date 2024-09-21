import cv2
import torch
from ultralytics import YOLOv10 as YOLO
import time

# Load the YOLOv10 model
model = YOLO('content_data3000_24-09-20/content/runs/detect/train/weights/last.pt')  # or another version of YOLOv8 (e.g., yolov8s.pt for small)

# Load the video file
input_video_path = '/Users/md/Developer/vespCV/test/dataSlider/hornet3000.m4v'

# Open the video using OpenCV
video_capture = cv2.VideoCapture(input_video_path)


# Get video properties
frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video_capture.get(cv2.CAP_PROP_FPS))
total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))


# Define variables
class_0_detected = False
last_class_0_time = None  # Time when class 0 was last detected
seconds = 5 # Cooldown time

# Iterate over each frame
frame_count = 0
while video_capture.isOpened():
    ret, frame = video_capture.read()  # Read a frame
    if not ret:
        break
    
    # Apply YOLOv8 object detection
    results = model(frame)[0]
    
    # Check for class 0 detection with high confidence
    for result in results.boxes.data.tolist():  # Each detection in the format [x1, y1, x2, y2, conf, class]
        x1, y1, x2, y2, conf, cls = result[:6]
        if cls == 0 and conf > 0.77:
            class_0_detected = True
            last_class_0_time = time.time()  # Update time of class 0 detection
            break

    # Save frame as JPG if class 0 detected and 5 minutes have passed
    if class_0_detected and (time.time() - last_class_0_time) >= seconds:
        image_name = f"detected_class_0_{frame_count}.jpg"
        cv2.imwrite(image_name, frame)
        print(f"Saved image: {image_name}")
        class_0_detected = False  # Reset flag after saving image

    # No need to write processed frame to video

    frame_count += 1
    print(f'Processed frame {frame_count}')

# Release resources
video_capture.release()
cv2.destroyAllWindows()

print(f'Finished processing video.')