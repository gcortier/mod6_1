import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from loguru import logger
from modules.calcul import calcul_carre
from modules.mnist import predict_digit, save_correction
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Gauge


## Base initialisation for Loguru and FastAPI
from api_mlflow import setup_loguru, app, Request, HTTPException
logger = setup_loguru("logs/main_api.log")

class NumberRequest(BaseModel):
    number: int

@app.post("/calcul")
def calcul(req: NumberRequest):
    result = calcul_carre(req.number)
    logger.info(f"Calcul du carré pour: {req.number} : result : {result}")
    return {"result": result}


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



@app.post("/correct")
async def correct(file: UploadFile = File(...), pred: int = Form(...), correction: int = Form(...)):
    logger.info(f"Received file for correction: {file.filename} : {pred} ==> {correction}")
   
   
    try:
        image_bytes = await file.read()
        save_correction(image_bytes, pred, correction, logger)
        return JSONResponse({"status": "ok"})
    except Exception as e:
        logger.error(f"Erreur during correction save : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde de la correction : {e}")



from training.train import train_model
from training.train_dl import train_dl_model

class TrainResponse(BaseModel):
    accuracy: float
    f1: float
    duration: float
    model_path: str
    cpu_usage: float = None

@app.post("/train")
def train_route(type: str = "ml"):
    """
    Lance l'entraînement du modèle ML ou DL selon le paramètre 'type'.
    Retourne les métriques principales.
    """
    try:
        if type == "ml":
            result = train_model()
        elif type == "dl":
            result = train_dl_model()
        else:
            raise HTTPException(status_code=400, detail="Type de modèle inconnu. Utilisez 'ml' ou 'dl'.")
        # Mise à jour des métriques Prometheus
        train_accuracy.labels(type=type).set(result["accuracy"])
        train_f1.labels(type=type).set(result["f1"])
        train_duration.labels(type=type).set(result["duration"])
        logger.info(f"Entraînement {type} terminé: {result}")
        return TrainResponse(**result)
    except Exception as e:
        logger.error(f"Erreur lors de l'entraînement {type}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Export automatisé des endpoints pour Prometheus
Instrumentator().instrument(app).expose(app)