import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# from fastapi import FastAPI, HTTPException
# from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
from modules import db_utils
import pandas as pd


## Base initialisation for Loguru and FastAPI
from api_base import setup_loguru, app, JSONResponse, FileResponse, UploadFile, Request, HTTPException, File
logger = setup_loguru("logs/api_database.log")

from modules.db_utils import get_session
from modules.models import Person


@app.get("/download-parquet")
def download_parquet():
    """
    Permet de télécharger le fichier Parquet complet contenant toutes les données.
    """
    parquet_path = "./adult/adult_all.parquet"
    try:
        if not os.path.exists(parquet_path):
            logger.error(f"Fichier Parquet non trouvé: {parquet_path}")
            raise HTTPException(status_code=404, detail="Fichier Parquet non trouvé.")
        logger.info(f"Téléchargement du fichier Parquet: {parquet_path}")
        return FileResponse(parquet_path, media_type="application/octet-stream", filename="adult_all.parquet")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement du fichier Parquet: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/person/latest")
def get_latest_persons():
    """
    Retourne les 5 dernières entrées de la table Person (tri décroissant par id).
    """
    try:
        session = get_session()
        latest = session.query(Person).order_by(Person.id.desc()).limit(5).all()
        # Formatage minimal (à adapter selon besoin)
        result = [
            {
                "id": p.id,
                "age": p.age,
                "workclass_id": p.workclass_id,
                "education_id": p.education_id,
                "marital_status_id": p.marital_status_id,
                "occupation_id": p.occupation_id,
                "capital_gain": p.capital_gain,
                "capital_loss": p.capital_loss,
                "hours_per_week": p.hours_per_week,
                "native_country_id": p.native_country_id,
                "class_label_id": p.class_label_id
            }
            for p in latest
        ]
        session.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

