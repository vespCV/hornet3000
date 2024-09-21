import cv2
import torch
import numpy as np
from ultralytics import YOLOv10 as YOLO

# Load the YOLOv10 model
model = YOLO('/Users/md/Developer/vespCV/content_data3000_24-09-20/runs/detect/train/weights/last.pt')  # or another version of YOLOv8 (e.g., yolov8s.pt for small)

# Load the video file
input_video_path = '/Users/md/Developer/vespCV/vespNonVesp24-09-20.mov'
output_video_path = 'test_mov_24-09-20.mp4'

# Open the video using OpenCV
video_capture = cv2.VideoCapture(input_video_path)

# Get video properties
frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video_capture.get(cv2.CAP_PROP_FPS))
total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

# Define the codec and create VideoWriter object to save output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
out_video = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# Iterate over each frame
frame_count = 0
while video_capture.isOpened():
    ret, frame = video_capture.read()  # Read a frame
    if not ret:
        break
    
    # Apply YOLOv8 object detection
    results = model(frame)[0]
    
    # Iterate through the detections and draw bounding boxes
    for result in results.boxes.data.tolist():  # Each detection in the format [x1, y1, x2, y2, conf, class]
        x1, y1, x2, y2, conf, cls = result[:6]
        class_name = model.names[cls]  # Extract class name
        confidence = conf  # Extract confidence score

        label = f'{class_name} {confidence:.2f}'  # Combine for display

        # Check for NaN values and convert to integers
        if not (np.isnan(x1) or np.isnan(y1)):
            x_int = int(x1)
            y_int = int(y1 - 10)
            org = (x_int, y_int)
            cv2.rectangle(frame, (x_int, int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)  # Bounding box
            cv2.putText(frame, label, org, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Print class number and confidence score (optional)
        print(f"Class: {class_name} (Index: {cls}), Confidence: {confidence:.2f}")

    # Write the processed frame to the output video
    out_video.write(frame)
    
    # Print progress
    frame_count += 1
    print(f'Processed frame {frame_count}/{total_frames}')

# Release resources
video_capture.release()
out_video.release()
cv2.destroyAllWindows()

print(f'Output video saved to {output_video_path}')