import cv2
import torch
from ultralytics import YOLOv10 as YOLO
import time

# Load the YOLOv10 model
model = YOLO('content_data3000_24-09-20/content/runs/detect/train/weights/last.pt')

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
cooldown_time = 5  # Cooldown in seconds
previous_conf = 0  # Previous confidence score for class 0
detection_start_time = None  # Time when confidence first exceeds 0.77
threshold_duration = 0.04  # 10 ms = 0.01 seconds

# Iterate over each frame
frame_count = 0
while video_capture.isOpened():
    ret, frame = video_capture.read()  # Read a frame
    if not ret:
        break

    # Apply YOLOv10 object detection
    results = model(frame)[0]

    # Check for class 0 detection with high confidence
    class_0_now_detected = False  # Reset class detection for each frame
    for result in results.boxes.data.tolist():  # Each detection in format [x1, y1, x2, y2, conf, class]
        x1, y1, x2, y2, conf, cls = result[:6]
        if cls == 0 and conf > 0.7:  # If class 0 is detected
            class_0_now_detected = True
            
            # Check if confidence crosses the threshold (above 0.77)
            if conf >= 0.77:
                if detection_start_time is None:  # Start the timer when the confidence first crosses 0.77
                    detection_start_time = time.time()
                elif (time.time() - detection_start_time) >= threshold_duration:  # Check if it stays above 0.77 for 10 ms
                    if last_class_0_time is None or (time.time() - last_class_0_time) >= cooldown_time:
                        # Save frame as JPG with timestamp
                        timestamp = time.strftime("%Y%m%d_%H%M%S")
                        image_name = f"VVN_{timestamp}.jpg"
                        cv2.imwrite(image_name, frame)
                        print(f"Saved image: {image_name}")
                        last_class_0_time = time.time()  # Update time of class 0 detection
                    detection_start_time = None  # Reset detection start time after saving the image
            else:
                detection_start_time = None  # Reset if confidence drops below 0.77
            previous_conf = conf  # Update previous confidence score
            break

    if not class_0_now_detected:
        previous_conf = 0  # Reset confidence if no class 0 detected in the frame
        detection_start_time = None  # Reset detection timer if class 0 is no longer detected

    frame_count += 1
    print(f'Processed frame {frame_count}')

# Release resources
video_capture.release()
cv2.destroyAllWindows()

print(f'Finished processing video.')

