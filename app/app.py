import os
import numpy as np
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing import image
from PIL import Image

app = Flask(__name__)

# Load the model
try:
    print("Loading model...")
    MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'Model', 'fruit_freshness_classifier.h5')
    # Use compile=False because we only need it for inference and don't need the optimizer state
    model = load_model(MODEL_PATH, compile=False)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def preprocess_image(img, target_size=(256, 256)):
    """
    Preprocesses the image for the model.
    1. Resize to target size.
    2. Convert to array.
    3. Expand dimensions to create batch.
    4. Rescale pixel values (1/255).
    """
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    img = img.resize(target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) # (1, 256, 256, 3)
    img_array = img_array / 255.0  # Rescale
    return img_array

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Open image directly from stream
        img = Image.open(file.stream)
        
        # Preprocess
        processed_img = preprocess_image(img)
        
        # Predict
        prediction = model.predict(processed_img)
        
        # Interpret result
        # Assuming class indices: {'fresh': 0, 'rotten': 1}
        # Model output shape is typically (1, 2) for softmax with 2 classes
        # or (1, 1) for sigmoid.
        # Based on notebook: preds = Dense(2, activation="softmax")(x)
        
        probabilities = prediction[0]
        fresh_score = probabilities[0]
        rotten_score = probabilities[1]
        
        if fresh_score > rotten_score:
            result = "Fresh"
            confidence = float(fresh_score)
        else:
            result = "Rotten"
            confidence = float(rotten_score)
            
        return jsonify({
            'result': result,
            'confidence': f"{confidence * 100:.2f}%",
            'fresh_prob': float(fresh_score),
            'rotten_prob': float(rotten_score)
        })

    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
