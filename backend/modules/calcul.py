from loguru import logger
import numpy as np
from PIL import Image
import io
import csv
import os

def calcul_carre(n: int) -> int:
    logger.info(f"Calcul du carré de {n}")
    return n * n

def predict_digit(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("L").resize((28, 28))
    arr = np.array(img).reshape(1, 28, 28, 1) / 255.0
    # TODO: Charger le vrai modèle et faire la prédiction
    # pred = model.predict(arr)
    # return int(np.argmax(pred))
    return 0  # Valeur fictive pour test

def save_correction(image_bytes, correction):
    if not os.path.exists("corrections.csv"):
        with open("corrections.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["image_bytes", "correction"])
    with open("corrections.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([image_bytes.hex(), correction])
