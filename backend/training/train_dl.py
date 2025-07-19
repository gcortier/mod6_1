import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import accuracy_score, f1_score
import time
import os
from loguru import logger
from utils.fetch_data import fetch_parquet, load_parquet
import psutil

DATABASE_API_URL = "http://database-app:8011/download-parquet"
MODEL_PATH = "models/model_dl.h5"


def preprocess_dl(df):
    df = df.dropna()
    X = df.drop("class_label", axis=1)
    y = df["class_label"]
    # Encodage simple
    X = pd.get_dummies(X)
    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    y_cat = to_categorical(y_enc)
    return X.values, y_cat


def train_dl_model():
    logger.info("Début du téléchargement du fichier Parquet...")
    parquet_path = fetch_parquet(DATABASE_API_URL, save_path="data/adult_all.parquet")
    df = load_parquet(parquet_path)
    logger.info(f"Données chargées: shape={df.shape}")
    X, y = preprocess_dl(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = Sequential([
        Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
        Dense(32, activation="relu"),
        Dense(y_train.shape[1], activation="softmax")
    ])
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    start = time.time()
    cpu_start = psutil.cpu_times().user
    model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=0)
    cpu_end = psutil.cpu_times().user
    duration = time.time() - start
    y_pred = model.predict(X_test)
    y_pred_labels = y_pred.argmax(axis=1)
    y_true_labels = y_test.argmax(axis=1)
    acc = accuracy_score(y_true_labels, y_pred_labels)
    f1 = f1_score(y_true_labels, y_pred_labels, average="weighted")
    model.save(MODEL_PATH)
    cpu_usage = cpu_end - cpu_start
    logger.info(f"Modèle DL entraîné et sauvegardé: {MODEL_PATH}")
    logger.info(f"Accuracy={acc:.4f}, F1={f1:.4f}, Durée entraînement={duration:.2f}s, CPU={cpu_usage:.2f}s")
    return {"accuracy": acc, "f1": f1, "duration": duration, "cpu_usage": cpu_usage, "model_path": MODEL_PATH}

if __name__ == "__main__":
    train_dl_model()
