import torch
import glob
import os
import pandas as pd

# Correct paths for your input and output folders
base_folder = './detection_workflow'  # Adjust as needed
input_folder = os.path.join(base_folder, 'input_images')
output_folder = os.path.join(base_folder, 'output_images')

# Ensure you've downloaded your 'best.pt' model file to an accessible location
model_path = '/Users/noahbakayou/Developer/Coding Projects/VSCodeProjects/AI/HackathonAIDoctor/yolov5/runs/train/exp/weights/best.pt'  # Update this to the actual path of your model file

# Load the model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

# List all images in the input folder (adjust the extension if needed)
input_images = glob.glob(os.path.join(input_folder, '*.jpg'))

# Verify if input images are found
if not input_images:
    raise ValueError("No images found in the input folder. Check the path or file extensions.")

# Run inference
results = model(input_images)

# Save the results to the output folder
# By default, YOLOv5's results are saved under 'runs/detect', to save in 'output_folder', we use the 'project' and 'name' arguments
results.save(save_dir=output_folder)

# Assume 'results' is the object returned by the YOLOv5 model after inference
detections = results.pandas().xyxy[0]  # Get detections for the first image in a DataFrame

# Initialize an empty list to store the formatted strings
detection_strings = []

# Iterate over each detection in the DataFrame
for index, row in detections.iterrows():
    # Format class name and confidence score
    detection_str = f"{row['name']} {row['confidence']:.2f}"
    # Append the formatted string to the list
    detection_strings.append(detection_str)

# Example: Join all detection strings into a single string, separated by commas
all_detections_str = ', '.join(detection_strings)
# Assume 'results' is the object returned by the YOLOv5 model after inference
detections = results.pandas().xyxy[0]  # Get detections for the first image in a DataFrame

# Initialize an empty list to store detection details
detection_details = []

# Iterate over each detection in the DataFrame
for index, row in detections.iterrows():
    # Extract and format the class name, confidence score, and bounding box coordinates
    detection_info = {
        "class_name": row['name'],
        "confidence": f"{row['confidence']:.2f}",
        "bbox": {
            "xmin": row['xmin'],
            "ymin": row['ymin'],
            "xmax": row['xmax'],
            "ymax": row['ymax']
        }
    }
    # Append the detection information to the list
    detection_details.append(detection_info)

# Example: Print detection details
for detail in detection_details:
    print(f"Class: {detail['class_name']}, Confidence: {detail['confidence']}, "
          f"BBox: [{detail['bbox']['xmin']:.0f}, {detail['bbox']['ymin']:.0f}, "
          f"{detail['bbox']['xmax']:.0f}, {detail['bbox']['ymax']:.0f}]")

