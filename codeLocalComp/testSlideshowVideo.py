# Input: weights of the model and slideshow in .m4v as surrogate for the camera to test the model
# Output: a video with bounding boxes, classes and confidence score
# Goal: check installed dependencies and adjust the tresholds 

import cv2
import torch
from ultralytics import YOLOv10 as YOLO

# Load the YOLOv10 model, copy path to last.pt in folder weights
model = YOLO('content_data3000_24-09-20/content/runs/detect/train/weights/last.pt')  # or another version of YOLOv8 (e.g., yolov8s.pt for small)

# Load the video file
input_video_path = '/Users/md/Developer/vespCV/test/dataSlider/hornet3000.m4v'
output_video_path = 'test_hornet3000_24-09-20.mp4'

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
        label = f'{model.names[cls]} {conf:.2f}'
        
        # Draw bounding box and label on the frame
        if conf > 0.77: 
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)  # Bounding box
                cv2.putText(frame, label, (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

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
