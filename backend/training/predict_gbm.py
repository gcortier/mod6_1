from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Any
import mlflow.sklearn
import pandas as pd
import requests
import io
import os

# DATABASE_API_URL = "http://database-app:8011"
DATABASE_API_URL = os.environ.get("DATABASE_API_URL", "http://localhost:8011")

# Liste des colonnes attendues (ordre et noms doivent correspondre au modèle)
GBM_FEATURES = [
    "DAY_OF_WEEK", "FL_DATE", "UNIQUE_CARRIER", "AIRLINE_ID", "ORIGIN", "DEST",
    "CRS_DEP_TIME", "DEP_TIME", "DEP_DELAY", "DEP_DEL15", "TAXI_OUT", "WHEELS_OFF",
    "CRS_ARR_TIME", "CRS_ELAPSED_TIME"
]

class FlightInput(BaseModel):
    DAY_OF_WEEK: int
    FL_DATE: int  # timestamp en secondes (déjà transformé)
    UNIQUE_CARRIER: str
    AIRLINE_ID: int
    ORIGIN: str
    DEST: str
    CRS_DEP_TIME: int
    DEP_TIME: int
    DEP_DELAY: float
    DEP_DEL15: int
    TAXI_OUT: float
    WHEELS_OFF: int
    CRS_ARR_TIME: int
    CRS_ELAPSED_TIME: float
    ARR_DEL15: Optional[int] = None  # Optionnel, pour comparaison

class FlightsBatch(BaseModel):
    data: List[FlightInput]

router = APIRouter()

mlFlowURL = os.environ.get("MLFLOW_TRACKING_URI", "http://localhost:5000")
print(f"MLFlow URL: {mlFlowURL}")

mlflow.set_tracking_uri(mlFlowURL)

# Utilisation du même nom d'artifact que pour l'entraînement (cohérence)
artifact_path = "gbm_model"
mlflow.set_experiment(artifact_path)


# Charger le pipeline complet MLflow (préprocessing + modèle)
MLFLOW_MODEL_URI = f"runs:/036311e1ec044052b08fba8e77bfc44e/{artifact_path}"
try:
    gbm_pipeline = mlflow.sklearn.load_model(MLFLOW_MODEL_URI)
except Exception as e:
    print("Erreur lors du chargement du modèle MLflow :", e)
    gbm_pipeline = None


# --- Fonction utilitaire pour tester la prédiction sur une donnée de test téléchargée ---
def load_predict_sample_fromparquet_test(api_url="http://localhost:8000"):
    """
    Télécharge le fichier de test via /download-parquet-test, sélectionne une ligne, la formate et l'envoie à /predict-gbm.
    """
    # 1. Télécharger le fichier Parquet de test
    url = f"{api_url}/download-parquet-test"
    print(f"Téléchargement du fichier de test depuis {url} ...")
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"Erreur lors du téléchargement: {resp.status_code}")
        return
    # 2. Charger le fichier Parquet en DataFrame
    try:
        df = pd.read_parquet(io.BytesIO(resp.content))
    except Exception:
        # Si c'est un CSV (parfois plus simple à manipuler)
        try:
            df = pd.read_csv(io.BytesIO(resp.content))
        except Exception as e:
            print(f"Erreur de lecture du fichier: {e}")
            return
    print(f"Fichier chargé: {df.shape[0]} lignes")
    # 3. Prendre une ligne au hasard
    row = df.sample(1, random_state=42).iloc[0]
    # 4. Formater pour FlightInput
    # On garde uniquement les colonnes attendues (plus ARR_DEL15 si présente)
    input_dict = {col: row[col] for col in GBM_FEATURES if col in row}
    if "ARR_DEL15" in row:
        input_dict["ARR_DEL15"] = int(row["ARR_DEL15"])
    # 5. Envoyer à la route de prédiction
    payload = {"data": [input_dict]}
    pred_url = f"{api_url}/predict-gbm"
    print(f"Envoi à {pred_url} ...")
    pred_resp = requests.post(pred_url, json=payload)
    if pred_resp.status_code != 200:
        print(f"Erreur prédiction: {pred_resp.status_code} {pred_resp.text}")
        return
    print("Résultat de la prédiction:")
    print(pred_resp.json())


@router.post("/predict-gbm")
def predict_gbm(batch: FlightsBatch):
    if gbm_pipeline is None:
        raise HTTPException(status_code=500, detail="Modèle non chargé")
    if batch is None:
        # batch = FlightsBatch(data=[])
        batch = load_predict_sample_fromparquet_test(DATABASE_API_URL)
    # Conversion en DataFrame
    df = pd.DataFrame([item.dict(exclude={"ARR_DEL15"}) for item in batch.data])
    preds = gbm_pipeline.predict(df)
    # Comparaison si vrai label fourni
    results = []
    for i, item in enumerate(batch.data):
        res = {
            "prediction": int(preds[i])
        }
        if item.ARR_DEL15 is not None:
            res["true"] = item.ARR_DEL15
            res["match"] = int(preds[i]) == item.ARR_DEL15
        results.append(res)
    return {"results": results}


# --- Exécution directe pour test rapide ---
if __name__ == "__main__":
    predict_gbm(None)
    
    #python -m training.predict_gbm