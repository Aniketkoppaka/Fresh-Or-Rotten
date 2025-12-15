# FreshCheck - Fruit Freshness Classifier 🍎🟣🍑

FreshCheck is a modern, user-friendly web application designed to instantly classify fruits as **Fresh** or **Rotten** using deep learning.

## Features ✨

*   **Multi-Fruit Support**: Accurate classification for Apples, Peaches, and Pomegranates.
*   **AI-Powered**: Uses a pre-trained TensorFlow/Keras model (MobileNetV2 based) for high accuracy.
*   **Interactive UI**:
    *   Drag & Drop image upload.
    *   3D Tilt effects on hover for an immersive experience.
    *   Confetti animations for "Fresh" results!
*   **Responsive Design**: Works on desktop and mobile.

## Tech Stack 🛠️

*   **Backend**: Flask (Python)
*   **Frontend**: HTML5, CSS3, Vanilla JavaScript
*   **ML Engine**: TensorFlow / Keras
*   **Image Processing**: Pillow (PIL), NumPy

## Installation & Setup 🚀

1.  **Prerequisites**: Ensure you have Python 3.8+ installed.

2.  **Clone/Download** the repository to your local machine.

3.  **Set up the Virtual Environment** (Recommended):
    ```bash
    # Windows
    python -m venv app/venv
    app\venv\Scripts\activate
    ```

4.  **Install Dependencies**:
    ```bash
    pip install -r app/requirements.txt
    ```

5.  **Run the Application**:
    ```bash
    python app/app.py
    ```

6.  **Open in Browser**:
    Navigate to `http://localhost:5000` to start using the classifier!

## Usage 📝

1.  Click the upload box or drag and drop an image of a fruit (JPG, PNG).
2.  The app will analyze the image and display the result:
    *   **Fresh**: Green theme + Confetti 🎉
    *   **Rotten**: Red theme + Warning ⚠️
3.  Click "Analyze Another" to reset and test a new image.

## Project Structure ​​​​

*   `app/`: Contains the main application code.
    *   `app.py`: Flask backend entry point.
    *   `static/`: CSS styles and JavaScript files.
    *   `templates/`: HTML templates.
    *   `test_model.py`: Script for manual model testing.
*   `Model/`: Stores the trained `.h5` model file.
*   `ModelTraining/`: Jupyter notebooks used for training the model.

---
