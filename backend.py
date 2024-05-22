# backend.py
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
import base64
from cryptography import encrypt, decrypt, calculate_rmse, calculate_psnr
import time

app = Flask(__name__, static_folder='frontend', static_url_path='')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/encrypt', methods=['POST'])
def encrypt_image():
    # Check if a file was uploaded
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Check file extension
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'})

    # Save the uploaded file temporarily
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Get other parameters from the request
    func = request.form['func']
    x0 = float(request.form['x0'])
    alpha = float(request.form['alpha'])
    beta = float(request.form['beta'])
    Omega = float(request.form['Omega'])
    K = float(request.form['K'])

    # Measure the execution time
    start_time = time.time()

    # Read input image as RGB matrix
    image_matrix = cv2.imread(file_path)

    # Perform encryption
    encrypted_image = encrypt(image_matrix, func, x0, alpha, beta, Omega, K)

    # Save the encrypted image to a temporary file
    encrypted_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encrypted_' + filename)
    cv2.imwrite(encrypted_image_path, encrypted_image)

    end_time = time.time()
    execution_time = end_time - start_time

    encryption_rmse = calculate_rmse(image_matrix, encrypted_image)
    encryption_psnr = calculate_psnr(image_matrix, encrypted_image)

    # Read the encrypted image as binary and convert it to base64 string
    with open(encrypted_image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Delete the temporary uploaded and encrypted image files
    os.remove(file_path)
    os.remove(encrypted_image_path)

    json_output = {
        'encrypted_image': encoded_image,
        'execution_time': execution_time,
        'calculated_rmse': encryption_rmse,
        'calculated_psnr': encryption_psnr
    }

    return jsonify(json_output)

@app.route('/decrypt', methods=['POST'])
def decrypt_image():
    # Check if a file was uploaded
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Check file extension
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'})

    # Save the uploaded file temporarily
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Get other parameters from the request
    func = request.form['func']
    x0 = float(request.form['x0'])
    alpha = float(request.form['alpha'])
    beta = float(request.form['beta'])
    Omega = float(request.form['Omega'])
    K = float(request.form['K'])

    # Measure the execution time
    start_time = time.time()

    # Read input image as RGB matrix
    image_matrix = cv2.imread(file_path)

    # Perform encryption
    decrypted_image = decrypt(image_matrix, func, x0, alpha, beta, Omega, K)

    # Save the encrypted image to a temporary file
    decrypted_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'decrypted_' + filename)
    cv2.imwrite(decrypted_image_path, decrypted_image)

    end_time = time.time()
    execution_time = end_time - start_time

    decryption_rmse = calculate_rmse(image_matrix, decrypted_image)
    decryption_psnr = calculate_psnr(image_matrix, decrypted_image)

    # Read the encrypted image as binary and convert it to base64 string
    with open(decrypted_image_path, 'rb') as image_file:
        decoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Delete the temporary uploaded and encrypted image files
    os.remove(file_path)
    os.remove(decrypted_image_path)
    
    json_output = {
        'decrypted_image': decoded_image,
        'execution_time': execution_time,
        'calculated_rmse': decryption_rmse,
        'calculated_psnr': decryption_psnr
    }

    return jsonify(json_output)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
