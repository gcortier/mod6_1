import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from loguru import logger
from modules.calcul import calcul_carre
from modules.mnist import predict_digit, save_correction
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Gauge

from typing import List, Optional, Any
import mlflow.sklearn
import pandas as pd
import requests
import io


## Base initialisation for Loguru and FastAPI
from api_mlflow import setup_loguru, app, Request, HTTPException
logger = setup_loguru("logs/main_api.log")

class NumberRequest(BaseModel):
    number: int

# @app.post("/calcul")
# def calcul(req: NumberRequest):
#     result = calcul_carre(req.number)
#     logger.info(f"Calcul du carré pour: {req.number} : result : {result}")
#     return {"result": result}


data_counter = Counter("data_value_total", "Compteur des valeurs reçues sur /data", ["value"])
correction_counter = Counter("correction_value_total", "Compteur des valeurs reçues sur /correct", ["value"])
train_accuracy = Gauge("train_accuracy", "Accuracy du modèle entraîné", ["type"])
train_f1 = Gauge("train_f1", "F1-score du modèle entraîné", ["type"])
train_duration = Gauge("train_duration_seconds", "Durée d'entraînement du modèle", ["type"])


@app.post("/data")
async def receive_color(data: str = Form(...)):
    logger.info(f"Received data: {data}")
    data_counter.labels(value=data).inc()
    return {"message": f"data {data} received"}



# @app.post("/correct")
# async def correct(file: UploadFile = File(...), pred: int = Form(...), correction: int = Form(...)):
#     logger.info(f"Received file for correction: {file.filename} : {pred} ==> {correction}")
   
   
#     try:
#         image_bytes = await file.read()
#         save_correction(image_bytes, pred, correction, logger)
#         return JSONResponse({"status": "ok"})
#     except Exception as e:
#         logger.error(f"Erreur during correction save : {e}")
#         raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde de la correction : {e}")



from training.train import train_model
from training.train_dl import train_dl_model, train_gbm_model

class TrainResponse(BaseModel):
    accuracy: float
    f1: float
    duration: float
    model_path: str
    cpu_usage: float = None

@app.post("/train")
def train_route(type: str = "gbm"):
    """
    Lance l'entraînement du modèle ML ou DL selon le paramètre 'type'.
    Retourne les métriques principales.
    """
    logger.info(f"train_route: {type}")
    try:
        if type == "ml":
            result = train_model()
        elif type == "dl":
            result = train_dl_model()
        elif type == "gbm":
            result = train_gbm_model()
        else:
            raise HTTPException(status_code=400, detail="Type de modèle inconnu. Utilisez 'ml', 'dl' ou 'gbm'")
        # Mise à jour des métriques Prometheus
        train_accuracy.labels(type=type).set(result["accuracy"])
        train_f1.labels(type=type).set(result["f1"])
        train_duration.labels(type=type).set(result["duration"])
        logger.info(f"Entraînement {type} terminé: {result}")
        return TrainResponse(**result)
    except Exception as e:
        logger.error(f"Erreur lors de l'entraînement {type}: {e}")
        raise HTTPException(status_code=500, detail=str(e))



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
@app.post("/load-predict-sample")
def load_predict_sample_fromparquet_test(api_url=DATABASE_API_URL):
    """
    Télécharge le fichier de test via /download-parquet-test, sélectionne une ligne, la formate et l'envoie à /predict-gbm.
    """
    logger.info(f"load_predict_sample_fromparquet_test: {api_url}")
    # 1. Télécharger le fichier Parquet de test
    
    url = f"{api_url}/download-parquet-test"
    logger.info(f"Téléchargement du fichier de test depuis {url} ...")
    resp = requests.get(url)
    if resp.status_code != 200:
        logger.error(f"Erreur lors du téléchargement: {resp.status_code}")
        return
    # 2. Charger le fichier Parquet en DataFrame
    try:
        df = pd.read_parquet(io.BytesIO(resp.content))
    except Exception as e:
        logger.error(f"Erreur de lecture du fichier: {e}")
        return
    logger.info(f"Fichier chargé: {df.shape[0]} lignes")
   
    
    try:
        # row = df.sample(1, random_state=42).iloc[0]
        row = df.sample(1).iloc[0]
        # Conversion des types pandas/numpy en types natifs Python
        def convert_value(val, col=None):
            import numpy as np
            if isinstance(val, (np.integer, int)):
                return int(val)
            elif isinstance(val, (np.floating, float)):
                return float(val)
            elif isinstance(val, pd.Timestamp):
                # Pour FL_DATE, retourne le timestamp en secondes
                if col == "FL_DATE":
                    return int(val.timestamp())
                else:
                    return val.strftime("%Y-%m-%d")
            else:
                return val

        input_dict = {col: convert_value(row[col], col) for col in GBM_FEATURES if col in row}
        if "ARR_DEL15" in row:
            input_dict["ARR_DEL15"] = int(row["ARR_DEL15"])
        payload = {"data": [input_dict]}
        logger.info(f"Payload: {payload} ...")
        return payload
    except Exception as e:
        logger.error("Erreur payload :", e)
        return {"data": []}

@app.post("/predict-gbm")
def predict_gbm(batch: FlightsBatch):
    logger.info(f"predict_gbm: {batch}")
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
            "prediction": int(preds[i]),
            "values": item.dict(exclude={"ARR_DEL15"})
        }
        if item.ARR_DEL15 is not None:
            res["true"] = item.ARR_DEL15
            res["match"] = int(preds[i]) == item.ARR_DEL15
        results.append(res)
    return {"results": results}





# Export automatisé des endpoints pour Prometheus
Instrumentator().instrument(app).expose(app)




# --- Exécution directe pour test rapide ---
if __name__ == "__main__":
    # predict_gbm(None)
    load_predict_sample_fromparquet_test(DATABASE_API_URL)