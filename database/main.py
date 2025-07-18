from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from modules import db_utils
import pandas as pd

app = FastAPI(title="API Database - Data & Stats Provider")

@app.get("/dataframe")
def get_dataframe():
    """
    Retourne l'ensemble des données d'entraînement/prédiction sous forme de DataFrame (JSON).
    """
    try:
        df = db_utils.fetch_full_dataframe()
        return JSONResponse(content=df.to_dict(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# À compléter : routes pour enregistrer les statistiques, etc.
