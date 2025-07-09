import numpy as np
from PIL import Image
import io
import csv
import os


def predict_digit(model, image_bytes, logger=None):
    # define default logger but expect a loguru logger is transmitted
    if logger is None:
        class DummyLogger:
            def info(self, msg):
                print(msg)
        logger = DummyLogger()
        
    
    logger.info(f"predict_digit")
    img = Image.open(io.BytesIO(image_bytes)).convert("L").resize((28, 28))
    arr = np.array(img).reshape(1, 28, 28, 1) / 255.0
    logger.info(f"arr : {arr}")
    pred = model.predict(arr)
    
    logger.info(f"Prediction : {pred} - {np.argmax(pred)}")
    
    return int(np.argmax(pred))

def save_correction(image_bytes, correction, logger=None):
    logger.info(f"save_correction : {correction}")
    if not os.path.exists("./data/user_corrections.csv"):
        with open("./data/user_corrections.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["image_bytes", "correction"])
    with open("./data/user_corrections.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([image_bytes.hex(), correction])
