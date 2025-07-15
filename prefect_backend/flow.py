import os
from prefect import flow, task
from prefect.logging import get_run_logger
import pandas as pd
# import optuna
from datetime import datetime
import requests


os.environ.setdefault("PYTHONIOENCODING", "utf-8")
os.environ.setdefault("PREFECT_API_URL", "http://127.0.0.1:4200/api")


@task(retries=2, retry_delay_seconds=1)
def retrain():
    logger = get_run_logger()
    logger.info("Retrain triggered!")
    raise Exception("Retrain failed!")  # Pour tester les retries

@task
def print_ok():
    logger = get_run_logger()
    logger.info("ok")

@task(retries=2, retry_delay_seconds=1)
def analyze_corrections(corrections_path: str, seuil_erreur: int = 5):

    logger = get_run_logger()
    
    logger.info(f"Analyse des corrections dans {corrections_path}")
    df = pd.read_csv(corrections_path)
 
 
    erreurs = df[df['pred'] != df['correction']]
    counts = erreurs['correction'].value_counts()
    logger.info(f"Nombre d'échecs par classe : {counts.to_dict()}")
    class_to_retrain = counts[counts > seuil_erreur].index.tolist()
    logger.info(f"Classes à réentraîner : {class_to_retrain}")
    return class_to_retrain

@task(retries=2, retry_delay_seconds=1)
def trigger_backend_retrain(class_to_retrain, corrections_path, base_data_path):

    logger = get_run_logger()

    if not class_to_retrain:
        logger.info("Aucune classe à réentraîner. Pas de réentraînement.")
        return "No retrain needed"
    logger.info(f"Déclenchement du réentraînement via l'API backend pour classes : {class_to_retrain}")
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000/retrain")
    payload = {
        "classes": class_to_retrain,
        "corrections_path": corrections_path,
        "base_data_path": base_data_path
    }
    try:
        response = requests.post(backend_url, json=payload)
        if response.ok:
            logger.info(f"Réentraînement backend lancé avec succès : {response.json()}")
            return response.json()
        else:
            logger.error(f"Erreur lors de l'appel backend : {response.text}")
            return None
    except Exception as e:
        logger.error(f"Exception lors de l'appel backend : {e}")
        return None

@flow
def periodic_check():
    corrections_path = os.getenv("CORRECTIONS_PATH", "data/user_corrections.csv")
    base_data_path = os.getenv("BASE_DATA_PATH", "data/mnist_full.csv")
    seuil_erreur = int(os.getenv("SEUIL_ERREUR", 5))
    class_to_retrain = analyze_corrections(corrections_path, seuil_erreur)
    trigger_backend_retrain(class_to_retrain, corrections_path, base_data_path)

if __name__ == "__main__":
    periodic_check.serve(
        name="every-hour",
        interval=360  # toutes les heures 3600
    )
