import torch
import glob
import os

# Assuming your Flask app runs from the 'yolov5' directory
base_folder = '/Users/noahbakayou/Developer/Coding Projects/VSCodeProjects/AI/HackathonAIDoctor/yolov5'
input_folder = os.path.join(base_folder, 'static/images')  # Updated path to match where Flask saves images

# This is where you want to save the processed images
# Let's save them in a subdirectory within 'static' to keep things organized
output_folder = os.path.join(base_folder, 'static/processed_images')
os.makedirs(output_folder, exist_ok=True)  # Ensure the output directory exists

model_path = '//Users/noahbakayou/Developer/Coding Projects/VSCodeProjects/AI/HackathonAIDoctor/yolov5/runs/train/exp/weights/best.pt' 

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

# List all images in the input folder
input_images = glob.glob(os.path.join(input_folder, '*.jpg'))

if not input_images:
    print("No images found in the input folder. Check the path or file extensions.")
else:
    # Run inference
    results = model(input_images)

    # Specify where to save processed images (YOLOv5 will create a 'runs/detect' directory by default)
    # We override this behavior by specifying 'project' and 'name' to control the output directory
    results.save(save_dir=output_folder)
