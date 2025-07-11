import sys
import mlflow
import json

from sklearn.model_selection import train_test_split
# from modules.preprocess import preprocessing_v2
from models.keras_mnist_models import model_predict, model_preprocess
import pandas as pd
import joblib
from os.path import join as join
from pydantic import BaseModel
from typing import List, Any
import numpy as np
import os

import pandas as pd
from os.path import join as join

from fastapi.responses import JSONResponse

from modules.mlflow_utils import MLFlow_load_model
from modules.mnist import predict_digit

from settings.mlflow_settings import settings, artifact_path, wanted_train_cycle


## Base initialisation for Loguru and FastAPI
from api_base import setup_loguru, app, UploadFile, Request, HTTPException, File

logger = setup_loguru("logs/api_mlflow.log")

from datetime import datetime
today_str = datetime.now().strftime("%Y%m%d_%H%M")

# Force url for MLFlow
logger.info(f"MLFlow tracking URI: {os.environ.get('MLFLOW_TRACKING_URI', 'http://localhost:5000')}")
mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://localhost:5000"))
mlflow.set_experiment(artifact_path)


# Utilitaire pour lire le run_id courant

def set_last_run_id(run_id):
    try:
        result = {
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "settings": settings,
            # futur : ajouter le r²
        }
        with open("models/current_model.json", "w") as f:
            json.dump(result, f)
        
        logger.info(f"Nouveau modèle de prédiction mis à jour avec run_id: {run_id} (sauvegardé dans models/current_model.json)")
                     
    except Exception:
        return ""
    
    
def get_last_run_id():
    try:
        with open("models/current_model.json", encoding="utf-8") as f:
            data = json.load(f)
            run_id = data.get("run_id", None)
            return None if run_id == "" else run_id
    except Exception:
        return None


prediction_model = get_last_run_id()  # Variable to hold the prediction model


### Function to train and log a model iteratively in MLFlow
def backup_preprocessor(settings):
    from modules.mlflow_utils import train_and_log_model
    
    """
    Entraîne un modèle et le log dans MLFlow, en utilisant un run_id pour charger un modèle précédent si disponible.
    """
    df = pd.read_csv(join('data', settings["training_data"]))
    logger.info(f"Proceed: {settings['training_data']} with shape {df.shape}")
    
    X_processed, y, preprocessor = model_preprocess(df, settings)
    
    joblib.dump(preprocessor, join('models', f'preprocessor_latest.pkl'))



    return preprocessor




### Function to train and log a model iteratively in MLFlow
def train_and_log_iterative(run_idx, settings, run_id=None):
    from modules.mlflow_utils import train_and_log_model
    
    """
    Entraîne un modèle et le log dans MLFlow, en utilisant un run_id pour charger un modèle précédent si disponible.
    """
    # df = pd.read_csv(join('data', settings["training_data"]))
    train_data_path = join('data', settings["training_data"])
    # clean data (duplicates, etc.)
    df = clean_dataset(train_data_path)
    
    logger.info(f"Training data loaded: {settings['training_data']} with shape {df.shape}")
    
    X_train, X_test, y_train, y_test = prepare_data(df, settings, run_idx)
    
    run_desc = f"Performance for run {run_idx}/{wanted_train_cycle}"
    run_id = train_and_log_model(X_train, y_train, X_test, y_test, run_desc, run_id, run_idx, artifact_path)
    
    return run_id

def prepare_data(df, settings, run_idx=0):
    """
    Prend un DataFrame, applique le préprocessing et split en train/test.
    Retourne X_train, X_test, y_train, y_test
    """
    X, y, _ = model_preprocess(df, settings)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state= 42+run_idx)  # Ajout de run_idx pour la reproductibilité
    return X_train, X_test, y_train, y_test
 


def clean_dataset(csv_path, csv_target=None):
    """
    Analyse le dataset, nettoie et sauvegarde le résultat.
    """
    df = pd.read_csv(csv_path)

    # Suppression des doublons
    df = df.drop_duplicates()
    # On vire car pas RGPD et pas éthique
    logger.info(f"Dataset shape after cleaning: {df.shape}")

    if csv_target:
        # Sauvegarde du dataset nettoyé si option
        df.to_csv(csv_target, index=False)
        
    return df
    
     


             
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "train":
        # python api_mlflow.py train
        # run_id = None
        run_id = prediction_model
        
        for i in range(wanted_train_cycle):
            logger.info(f"Starting training iteration {i} of {wanted_train_cycle}")
            run_id = train_and_log_iterative(i, settings, run_id)
        # Mettre à jour le modèle de prédiction avec le dernier run_id
        set_last_run_id(run_id)

        
    else:
        print("Aucune action lancée. Pour entraîner, lancez : python alchemy_api.py train")


class PredictRequest(BaseModel):
    data: List[Any]  

class RetrainRequest(BaseModel):
    data_path: str  # Chemin du fichier CSV à utiliser comme nouvelle source de données
    from_existing_model: bool = True  # True: fine-tuning, False: nouveau modèle

class RetrainResponse(BaseModel):
    status: str
    run_id: str




@app.get("/current_model")
async def current_model(request: Request):
    """
    Endpoint pour obtenir le run_id du modèle courant.
    """
    logger.info(f"Route '{request.url.path}' called by {request.client.host}")
    run_id = get_last_run_id()
    if not run_id:
        raise HTTPException(status_code=404, detail="Aucun modèle courant trouvé.")
    
    return {"run_id": run_id}



@app.post("/predict",)
async def predict(file: UploadFile = File(...)):
    """
    Endpoint pour effectuer des prédictions.
    """
    run_id = get_last_run_id()
    model_uri = f"runs:/{run_id}/{artifact_path}"
    logger.info(f"Received file for prediction: {file.filename} => Checking model URI {model_uri}")
    if not mlflow.get_artifact_uri(model_uri):
        logger.error(f"Model URI {model_uri} not found in MLflow.")
        return None
    
    if not run_id:
        logger.error("Aucun run_id disponible pour la prédiction. Entraînez un modèle d'abord.")
        raise HTTPException(status_code=404, detail="Aucun modèle courant trouvé. Veuillez entraîner un modèle avant de prédire.")
    
    # logger.info(f"Transmitting weights from model at {model_uri} to new model.")
    
   
    model = MLFlow_load_model(run_id, artifact_path)
    logger.info(f"ModelMLFlow Loaded")
    image_bytes = await file.read()
    prediction = predict_digit(model, image_bytes, logger=logger)
    return {"prediction": prediction}
    # return JSONResponse({"prediction": prediction})

@app.post("/train",)
async def train():
    """
    Endpoint pour entraîner un modèle.
    """

    run_id = prediction_model
        
    try:
        for i in range(wanted_train_cycle):
            logger.info(f"Starting training iteration {i} of {wanted_train_cycle}")
            run_id = train_and_log_iterative(i, settings, run_id)
        # Mettre à jour le modèle de prédiction avec le dernier run_id
        set_last_run_id(run_id)
        return {"status": "success", "run_id": run_id}
    except Exception as e:
        logger.error(f"Erreur lors de l'entraînement : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'entraînement : {e}")
