import numpy as np
import pandas as pd
from PIL import Image
import io
import csv
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def predict_digit(model, image_bytes, logger=None):
    # define default logger but expect a loguru logger is transmitted
    if logger is None:
        class DummyLogger:
            def info(self, msg):
                print(msg)
        logger = DummyLogger()
        
    
    # logger.info(f"predict_digit")
    img = Image.open(io.BytesIO(image_bytes)).convert("L").resize((28, 28))
    arr = np.array(img).reshape(1, 28, 28, 1) / 255.0

    pred = model.predict(arr)
    
    logger.info(f"Prediction : {pred} - {np.argmax(pred)}")
    
    return int(np.argmax(pred))

def save_correction(image_bytes, pred, correction, logger=None):
    logger.info(f"save_correction : {correction}")
    # Write header if the file does not exist
    if not os.path.exists("./data/user_corrections.csv"):
        with open("./data/user_corrections.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["image_bytes", "pred", "correction"])
    
    with open("./data/user_corrections.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([image_bytes.hex(), pred, correction])


def increase_correction(df_corr, n_aug=1, rotation_range=15):
    """
    Pour chaque image hexadécimale, génère n_aug images augmentées par rotation (ImageDataGenerator).
    Retourne un DataFrame format MNIST (784 colonnes de pixels + target).
    """
    # pixel_columns = [f"px_{i}" for i in range(28*28)]
    pixel_columns = [str(i) for i in range(28*28)]
    data = []
    datagen = ImageDataGenerator(rotation_range=rotation_range)
    
    for idx, row in df_corr.iterrows():
        hex_str = row["image_bytes"]
        target = row["target"]
        # Décoder l'image hexadécimale
        img_bytes = bytes.fromhex(hex_str)
        img = Image.open(io.BytesIO(img_bytes)).convert("L").resize((28, 28))
        arr = np.array(img)
        # Ajouter l'originale
        data.append(np.append(arr.flatten(), target))
        # Générer des images augmentées
        arr_expanded = arr.reshape((1, 28, 28, 1)) / 255.0  # normalisé pour ImageDataGenerator
        aug_iter = datagen.flow(arr_expanded, batch_size=1)
        for _ in range(n_aug):
            arr_aug = next(aug_iter)[0]  # shape (28,28,1), valeurs [0,1]
            arr_aug = (arr_aug * 255).astype(np.uint8).reshape(28, 28)
            data.append(np.append(arr_aug.flatten(), target))
    df_final = pd.DataFrame(data, columns=pixel_columns + ["target"])
    return df_final