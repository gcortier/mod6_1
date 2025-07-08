import numpy as np
from PIL import Image
import io
import csv
import os
from tensorflow import keras

# Charger le modèle Keras une seule fois au démarrage
MODEL_PATH = os.getenv("MNIST_MODEL_PATH", "mnist_cnn.h5")
try:
    model = keras.models.load_model(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Erreur lors du chargement du modèle Keras: {e}")

def predict_digit(image_bytes):
    if model is None:
        raise RuntimeError("Modèle MNIST non chargé")
    img = Image.open(io.BytesIO(image_bytes)).convert("L").resize((28, 28))
    arr = np.array(img).reshape(1, 28, 28, 1) / 255.0
    pred = model.predict(arr)
    return int(np.argmax(pred))

def save_correction(image_bytes, correction):
    if not os.path.exists("user_corrections.csv"):
        with open("user_corrections.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["image_bytes", "correction"])
    with open("user_corrections.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([image_bytes.hex(), correction])
