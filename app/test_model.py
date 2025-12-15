import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing import image

def test_model():
    print("Testing model prediction...")
    
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, '..', 'Model', 'fruit_freshness_classifier.h5')
    
    # Load model
    try:
        model = load_model(model_path, compile=False)
        print("Model loaded.")
    except Exception as e:
        print(f"Failed to load model: {e}")
        return

    # Helper to predict
    def predict_image(img_path, expected_label):
        try:
            img = image.load_img(img_path, target_size=(256, 256))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = x / 255.0  # Rescale
            
            preds = model.predict(x)
            print(f"\nImage: {os.path.basename(img_path)}")
            print(f"Expected: {expected_label}")
            print(f"Raw Output: {preds}")
            
            # Assuming [fresh, rotten]
            fresh_prob = preds[0][0]
            rotten_prob = preds[0][1]
            
            predicted = "Fresh" if fresh_prob > rotten_prob else "Rotten"
            print(f"Predicted: {predicted} (Fresh: {fresh_prob:.4f}, Rotten: {rotten_prob:.4f})")
            
            if predicted.lower() == expected_label.lower():
                print("✅ PASSED")
            else:
                print("❌ FAILED")
                
        except Exception as e:
            print(f"Error predicting {img_path}: {e}")

    # Test cases - placeholders, will be replaced by actual paths found in next step if needed, 
    # but I'll try to find them dynamically or just hardcode if I see the list output.
    # checking list output...
    
    fresh_dir = os.path.join(base_dir, '..', 'Fruits-Dataset', 'fresh', 'peaches')
    rotten_dir = os.path.join(base_dir, '..', 'Fruits-Dataset', 'rotten', 'peaches')
    
    # Get first file from each
    if os.path.exists(fresh_dir) and os.listdir(fresh_dir):
        fresh_img = os.path.join(fresh_dir, os.listdir(fresh_dir)[0])
        predict_image(fresh_img, "Fresh")
    else:
        print("Could not find fresh peach image.")

    if os.path.exists(rotten_dir) and os.listdir(rotten_dir):
        rotten_img = os.path.join(rotten_dir, os.listdir(rotten_dir)[0])
        predict_image(rotten_img, "Rotten")
    else:
        print("Could not find rotten peach image.")

if __name__ == "__main__":
    test_model()
