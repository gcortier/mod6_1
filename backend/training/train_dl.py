import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

import time
import os
import mlflow
import mlflow.keras
from loguru import logger
from utils.fetch_data import fetch_parquet, load_parquet
import psutil

from lightgbm import LGBMClassifier
import joblib



DATABASE_API_URL = "http://database-app:8011/download-parquet"
MODEL_PATH = "models/model_dl.h5"
MODEL_GBM_PATH = "models/model_gbm.pkl"


def preprocess_dl(df):
    df = df.dropna()
    X = df.drop("class_label", axis=1)
    y = df["class_label"]
    # Encodage simple
    X = pd.get_dummies(X)
    X = X.astype("float32")  # Conversion explicite pour Keras
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
    with mlflow.start_run():
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
        # Log MLflow params, metrics, and model
        mlflow.log_param("epochs", 20)
        mlflow.log_param("batch_size", 32)
        mlflow.log_param("optimizer", "adam")
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1", f1)
        mlflow.log_metric("duration", duration)
        mlflow.log_metric("cpu_usage", cpu_usage)
        mlflow.keras.log_model(model, "model")
        logger.info(f"Modèle DL entraîné et sauvegardé: {MODEL_PATH}")
        logger.info(f"Accuracy={acc:.4f}, F1={f1:.4f}, Durée entraînement={duration:.2f}s, CPU={cpu_usage:.2f}s")
    return {"accuracy": acc, "f1": f1, "duration": duration, "cpu_usage": cpu_usage, "model_path": MODEL_PATH}



def preprocess_gbm(df):
    df = df.dropna()
    


    # Conversion du datetime en timestamp pour garder une information temporelle
    df["FL_DATE"] = df["FL_DATE"].astype("int64") // 10**9  # en secondes

    # Préparation des données : X = toutes les colonnes sauf ARR_DEL15, y = ARR_DEL15
    y = df['ARR_DEL15'].astype(int)
    X = df.drop(columns=['ARR_DEL15'])
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Détection automatique des colonnes numériques et catégorielles
    colonnes_numeriques = X.select_dtypes(include=[np.number]).columns.tolist()
    #colonnes_categorielles : UNIQUE_CARRIER / ORIGIN AIRPORT / DESTINATION AIRPORT
    colonnes_categorielles = X.select_dtypes(exclude=[np.number]).columns.tolist()

    return X_train, X_test, y_train, y_test, colonnes_numeriques, colonnes_categorielles


def build_pipeline_gbm(col_num, col_cat):
    preprocesseur = ColumnTransformer([
        ('num', StandardScaler(), col_num),
        ('cat', OneHotEncoder(handle_unknown='ignore'), col_cat)
    ])
    model = LGBMClassifier(
        n_estimators=300, 
        learning_rate=0.1, 
        random_state=42,
        # Utilisation de l'argument class_weight pour équilibrer les classes
        class_weight='balanced'
        )
    return Pipeline([
        ('preprocessing', preprocesseur),
        ('clf', model)
    ])


def train_gbm_model():
    logger.info("Début du téléchargement du fichier Parquet...")
    parquet_path = fetch_parquet(DATABASE_API_URL, save_path="data/flights_train.parquet")
    df = load_parquet(parquet_path)
    logger.info(f"Données chargées: shape={df.shape}")
    # Prétraitement des données
    X_train, X_test, y_train, y_test, colonnes_numeriques, colonnes_categorielles = preprocess_gbm(df)

    artifact_path = "gbm_model"  # Nom d'artifact cohérent pour entraînement et prédiction
    mlflow.set_experiment(artifact_path)
    

    with mlflow.start_run():
        start = time.time()
        cpu_start = psutil.cpu_times().user
        
        
        pipeline = build_pipeline_gbm(colonnes_numeriques, colonnes_categorielles)
        pipeline.fit(X_train, y_train)
        
        # model = lgb.LGBMClassifier(random_state=42, n_estimators=100)
        # model.fit(X_train, y_train)
        
        cpu_end = psutil.cpu_times().user
        duration = time.time() - start
        y_pred = pipeline.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")
        cpu_usage = cpu_end - cpu_start
        # Log MLflow params, metrics, and model
        mlflow.log_param("n_estimators", 300)
        mlflow.log_param("random_state", 42)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1", f1)
        mlflow.log_metric("duration", duration)
        mlflow.log_metric("cpu_usage", cpu_usage)
        # On log le pipeline complet (préprocessing + modèle) pour garantir la reproductibilité à l'inférence
        mlflow.sklearn.log_model(pipeline, artifact_path)
        # sauvegarde locale
        joblib.dump(pipeline, MODEL_GBM_PATH)
        logger.info(f"Modèle LightGBM entraîné et sauvegardé.")
        logger.info(f"Accuracy={acc:.4f}, F1={f1:.4f}, Durée entraînement={duration:.2f}s, CPU={cpu_usage:.2f}s")
    return {"accuracy": acc, "f1": f1, "duration": duration, "cpu_usage": cpu_usage, "model_path": MODEL_GBM_PATH}





if __name__ == "__main__":
    train_gbm_model()
