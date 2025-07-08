import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


from fastapi import FastAPI, Form
from pydantic import BaseModel
from loguru import logger
from modules.calcul import calcul_carre
from prometheus_fastapi_instrumentator import Instrumentator


## Base initialisation for Loguru and FastAPI
from api_base import setup_loguru, app, Request, HTTPException
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

# Export automatisé des endpoints pour Prometheus
Instrumentator().instrument(app).expose(app)