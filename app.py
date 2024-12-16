from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

# Konfigurasi folder upload
UPLOAD_FOLDER = './uploads'  # Pastikan folder dibuat
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Fungsi untuk validasi ekstensi file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Fungsi untuk membaca class labels dari file label.txt
def load_class_labels():
    label_path = os.path.join('model', 'label.txt')
    with open(label_path, 'r') as file:
        class_labels = [line.strip() for line in file]
    return class_labels

# Fungsi untuk analisis gambar
def analyze_image(filepath):
    model_path = os.path.join('model', 'cnn_model_final.h5')
    model = tf.keras.models.load_model(model_path)
    
    class_labels = load_class_labels()
    img = image.load_img(filepath, target_size=(200, 200))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    predicted_class = class_labels[np.argmax(prediction)]
    return predicted_class

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Pastikan folder ada
            
            file.save(filepath)
            prediction_result = analyze_image(filepath)
            file_url = url_for('uploaded_file', filename=filename)
            return jsonify({
                'filename': filename,
                'file_url': file_url,
                'prediction': prediction_result  # Kirim hasil prediksi sebagai string
            })
    return render_template("index.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=8080, debug=True)