import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import joblib
import time
from loguru import logger
import mlflow
import mlflow.sklearn
from utils.fetch_data import fetch_parquet, load_parquet
import psutil


DATABASE_API_URL = "http://database-app:8011/download-parquet"
MODEL_PATH = "models/model_rf.pkl"


def preprocess(df):
    # Exemple minimal : drop NA, encode catégoriel
    df = df.dropna()
    X = df.drop("class_label", axis=1)
    y = df["class_label"]
    # Encodage simple (à adapter)
    X = pd.get_dummies(X)
    return X, y


def train_model():
    logger.info("Début du téléchargement du fichier Parquet...")
    parquet_path = fetch_parquet(DATABASE_API_URL)
    df = load_parquet(parquet_path)
    logger.info(f"Données chargées: shape={df.shape}")
    X, y = preprocess(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    with mlflow.start_run():
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        logger.info(f"Type du modèle instancié: {type(model)}")
        if model is None:
            logger.error("Le modèle RandomForestClassifier n'a pas été instancié correctement.")
            raise ValueError("Le modèle est None.")
        start = time.time()
        cpu_start = psutil.cpu_times().user
        model.fit(X_train, y_train)
        cpu_end = psutil.cpu_times().user
        duration = time.time() - start
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")
        cpu_usage = cpu_end - cpu_start
        joblib.dump(model, MODEL_PATH)
        # Log MLflow params, metrics, and model
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("random_state", 42)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1", f1)
        mlflow.log_metric("duration", duration)
        mlflow.log_metric("cpu_usage", cpu_usage)
        mlflow.sklearn.log_model(model, "model")
        logger.info(f"Modèle entraîné et sauvegardé: {MODEL_PATH}")
        logger.info(f"Accuracy={acc:.4f}, F1={f1:.4f}, Durée entraînement={duration:.2f}s")
    return {"accuracy": acc, "f1": f1, "duration": duration, "model_path": MODEL_PATH}

if __name__ == "__main__":
    train_model()
