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
from flights.data.models import Flight


@app.get("/download-parquet")
def download_parquet():
    """
    Permet de télécharger le fichier Parquet complet contenant toutes les données.
    """

    # parquet_path = "./flights/data/all_cleaned.parquet"
    parquet_path = "./flights/data/processed/sample_cleaned.parquet"
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

@app.get("/flights/latest")
def get_latest_flights():
    """
    Retourne les 5 dernières entrées de la table Flight (tri décroissant par id).
    """
    try:
        session = get_session()
        latest = session.query(Flight).order_by(Flight.id.desc()).limit(5).all()
        # Formatage minimal (à adapter selon besoin)
        result = [
            {
                "id": f.id,
                "flight_date": f.flight_date,
                "day_of_week": f.day_of_week,
                # "flight_number": f.flight_number,
                "carrier_id": f.carrier_id,
                "origin_id": f.origin_id,
                "dest_id": f.dest_id,
                "dep_time_blk_id": f.dep_time_blk_id,
                "arr_time_blk_id": f.arr_time_blk_id,
                "crs_dep_time": f.crs_dep_time,
                "dep_time": f.dep_time,
                "dep_delay": f.dep_delay,
                "dep_delay_new": f.dep_delay_new,
                "dep_del15": f.dep_del15,
                "dep_delay_group": f.dep_delay_group,
                "taxi_out": f.taxi_out,
                "wheels_off": f.wheels_off,
                # "wheels_on": f.wheels_on,
                # "taxi_in": f.taxi_in,
                # "crs_arr_time": f.crs_arr_time,
                # "arr_time": f.arr_time,
                # "arr_delay": f.arr_delay,
                # "arr_delay_new": f.arr_delay_new,
                "arr_del15": f.arr_del15,
                # "arr_delay_group": f.arr_delay_group,
                # "cancelled": f.cancelled,
                # "cancellation_code": f.cancellation_code,
                # "diverted": f.diverted,
                # "crs_elapsed_time": f.crs_elapsed_time,
                # "actual_elapsed_time": f.actual_elapsed_time,
                # "air_time": f.air_time
            }
            for f in latest
        ]
        session.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

