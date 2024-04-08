from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import glob
from werkzeug.utils import secure_filename
from detect_local import *

app = Flask(__name__)

# Base directory for uploading and serving processed images
UPLOAD_FOLDER = 'static/images'
PROCESSED_FOLDER_BASE = 'static'
PROCESSED_FOLDER = os.path.join(PROCESSED_FOLDER_BASE, 'processed_images*')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
global response
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Assuming detect_local.py is set up to read from UPLOAD_FOLDER and write to a processed_images* directory
            # Adjust the subprocess command as necessary
            response = model()

            return redirect(url_for('upload_file'))

    # Find the latest processed_images* directory
    processed_dirs = glob.glob(PROCESSED_FOLDER)
    latest_dir = max(processed_dirs, key=os.path.getmtime, default=None)

    latest_image_url = None
    if latest_dir:
        # Find the latest image within that directory
        latest_image = max(glob.glob(os.path.join(latest_dir, '*.jpg')), key=os.path.getmtime, default=None)
        if latest_image:
            # Generate the relative path for HTML use
            latest_image_url = os.path.relpath(latest_image, PROCESSED_FOLDER_BASE)

    return render_template('upload.html', latest_image_url=latest_image_url)

@app.route('/generate_response', methods=['POST'])
def generate_response_route():
    print('hiii')
    return jsonify({'response': response})
if __name__ == '__main__':
    app.run(debug=True, port=7000)
