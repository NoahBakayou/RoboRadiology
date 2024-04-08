import torch
import glob
import os
from response import generate_response
from file import *

def create_json(folder_name):
    folder = os.getcwd() + '/' + folder_name
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    return folder



def model():
    create_json('db')
    db = JSON_Database('db/database')

    response_class = 'response'
    db.add_class(response_class)
    
    # Assuming your Flask app runs from the 'yolov5' directory
    base_folder = os.getcwd()
    input_folder = os.path.join(base_folder, 'static/images')  # Updated path to match where Flask saves images

    # This is where you want to save the processed images
    output_folder = os.path.join(base_folder, 'static/processed_images')
    os.makedirs(output_folder, exist_ok=True)  # Ensure the output directory exists

    model_path =  base_folder + '/runs/train/exp/weights/best.pt'

    # Load the YOLOv5 model
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

    # List all images in the input folder
    input_images = glob.glob(os.path.join(input_folder, '*.jpg'))

    if not input_images:
        print("No images found in the input folder. Check the path or file extensions.")
    else:
        confidence = ''
        issue = ''
        # Run inference
        results = model(input_images)

        # Access class names
        class_names = model.module.names if hasattr(model, 'module') else model.names

        # Process each detection

        for img_path, img_detections in zip(input_images, results.pred):
            print(f"Detections for {img_path}:")
            for *box, conf, cls_id in img_detections:
                x1, y1, x2, y2 = box
                # Use cls_id to get the class name
                class_name = class_names[int(cls_id)]
                # print(f"Bounding box: [{x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f}], Confidence: {conf:.2f}, Class: {class_name}")
                confidence = f"Confidence: {conf:.2f}"
                issue = f"Class: {class_name}"

        # Saving processed images to the specified output directory
        # We use 'save_dir' to directly specify the output folder
        results.save(save_dir=output_folder)

        response = generate_response(confidence, issue)
        db.add_data(response_class, response)
        # print(response)
        return response

if __name__ == '__main__':
    print('hello')