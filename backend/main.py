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


from prometheus_client import Counter
data_counter = Counter("data_value_total", "Compteur des valeurs reçues sur /data", ["value"])


@app.post("/data")
async def receive_color(data: str = Form(...)):
    logger.info(f"Received data: {data}")
    data_counter.labels(value=data).inc()
    return {"message": f"data {data} received"}

# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     logger.info(f"Received file for prediction: {file.filename}")
    
#     model_uri = f"runs:/{run_id}/{artifact_path}"
#     if not mlflow.get_artifact_uri(model_uri):
#         logger.error(f"Model URI {model_uri} not found in MLflow.")
#         return None
    
    
#     logger.info(f"Transmitting weights from model at {model_uri} to new model.")
    
    
    
#     model_old = MLFlow_load_model(model_uri, artifact_path)
    
#     image_bytes = await file.read()
#     prediction = predict_digit(image_bytes)
#     return JSONResponse({"prediction": prediction})

@app.post("/correct")
async def correct(file: UploadFile = File(...), correction: int = Form(...)):
    logger.info(f"Received file for correction: {file.filename} : {correction}")
    image_bytes = await file.read()
    save_correction(image_bytes, correction)
    return JSONResponse({"status": "ok"})

# Export automatisé des endpoints pour Prometheus
Instrumentator().instrument(app).expose(app)