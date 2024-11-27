# find duplicates by using histogram (to handle possible compression by gbif)

import cv2
import os

def compare_histograms(img1, img2):
    hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
    score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return score

def find_similar_histograms(directory, threshold=0.9):
    images = {}
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(directory, filename)
            images[filename] = cv2.imread(filepath, 0)  # Read in grayscale
    
    duplicates = []
    filenames = list(images.keys())
    for i in range(len(filenames)):
        for j in range(i + 1, len(filenames)):
            sim = compare_histograms(images[filenames[i]], images[filenames[j]])
            if sim > threshold:
                duplicates.append((filenames[i], filenames[j]))
    return duplicates

duplicates = find_similar_histograms('/Users/md/Downloads/amel.v1i.yolov11/train/images')
for img1, img2 in duplicates:
    print(f"Similar images: {img1}, {img2}")
