from flask import Flask, render_template, request, redirect, url_for
import os
import glob
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = '/Users/noahbakayou/Developer/Coding Projects/VSCodeProjects/AI/HackathonAIDoctor/yolov5/detection_workflow/input_images'
OUTPUT_BASE_FOLDER = '/Users/noahbakayou/Developer/Coding Projects/VSCodeProjects/AI/HackathonAIDoctor/yolov5/detection_workflow'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            
            # Assuming detect_local.py processes the image and saves it
            subprocess.run(['python', 'detect_local.py', file_path], check=True)

            # Redirect to GET to show the latest image
            return redirect(url_for('upload_file'))
    
    # Find the most recent output directory
    latest_dir = max(glob.glob(os.path.join(OUTPUT_BASE_FOLDER, 'output_images*')), key=os.path.getmtime, default=None)
    if latest_dir:
        # Find the first image in the directory
        latest_image = next(iter(glob.glob(os.path.join(latest_dir, '*.*'))), None)
        if latest_image:
            # Make the path relative to the static directory to serve it
            # Assuming 'static' is a symlink or otherwise maps to your 'detection_workflow'
            latest_image_url = os.path.relpath(latest_image, 'static')
        else:
            latest_image_url = None
    else:
        latest_image_url = None

    return render_template('upload.html', latest_image_url=latest_image_url)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
