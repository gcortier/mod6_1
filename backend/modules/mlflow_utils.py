import mlflow
import mlflow.sklearn
import joblib
from os.path import join as join
from datetime import datetime
from models.keras_mnist_models import create_nn_model, train_model, model_evaluate, model_predict, draw_loss, print_data
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

import pandas as pd

from settings.mlflow_settings import settings, artifact_path, wanted_train_cycle
from api_base import setup_loguru

# Initialisation de Loguru
logger = setup_loguru("logs/mlflow_utils.log")


today_str = datetime.now().strftime("%Y%m%d_%H%M")


def MLFlow_train_model(model, X, y, X_test=None, y_test=None, epochs=50, batch_size=32, verbose=0):
    # entrainnement du modèle
    model, hist = train_model(model, X, y, X_test, y_test, epochs, batch_size, verbose)
       
    return model, hist

def MLFlow_load_model(runId, artifactPath="linear_regression_model"):
    model_uri = f"runs:/{runId}/{artifactPath}"

    try:
        import sklearn.base
        if isinstance(model, sklearn.base.BaseEstimator):
            model = mlflow.sklearn.load_model(model_uri)
            logger.info("Model sklearn loaded with mlflow.sklearn")
        else:
            import tensorflow as tf
            if isinstance(model, tf.keras.Model):
                model = mlflow.keras.log_model(model_uri)
                logger.info("Model keras loaded with mlflow.keras")
            else:
                logger.error(f"Type de modele non supported MLflow: {type(model)}")
    except Exception as e:
        logger.error(f"Erreur lors du log du modèle dans MLflow: {e}")


    # model = mlflow.keras.load_model(model_uri)
    return model

def MLFlow_make_prediction(model, X):
    return model_predict(model, X)

def train_and_log_model(X_train, y_train, X_test, y_test, run_desc, model_id=None, run_idx=0, artifact_path="linear_regression_model"):
    """
    Entraîne un modèle, loggue dans MLflow, retourne le model_id.
    """
    
    epochs = settings.get("epochs", 50)
    batch_size = settings.get("batch_size", 32)
    
    
     # Charger le modèle du run précédent ou créer un nouveau modèle
    if model_id is not None:
        logger.info(f"Loading model from previous model_id: {model_id}")
        model = MLFlow_load_model(model_id, artifact_path)
    else:
        logger.info(f"No previous model_id, Trainning column : {X_train.shape[1]}")
        model = create_nn_model(X_train.shape[1])
        model_id = "None"  # Reset model_id if no previous model is loaded
    
    
    # Bascule des poids de models si existants dans le settings
    if settings.get("transfert_weights", {}).get("active", False):
        logger.info(f"Transferring weights from previous model_id: {settings['transfert_weights']['run_id']}")
        if not model_id or model_id == "None":
            logger.warning("No previous model_id provided for weight transfer.")
        else:
            # Transfert des poids du modèle existant vers le nouveau modèle
            MLFlow_Transmit_weights(model, settings['transfert_weights']['run_id'], artifact_path)
    
    ## TRAINING ET LOGGING DU MODÈLE
    

    model, hist = MLFlow_train_model(model, X_train, y_train, X_test=X_test, y_test=y_test, epochs=epochs, batch_size=batch_size, verbose=0)


    
    # Evaluation
    loss, accuracy = model_evaluate(model, X_test, y_test)
    print_data(loss, accuracy)
    logger.info(f"Model performances: {loss}")
    
    # Log dans MLflow
    if mlflow.active_run() is not None:
        mlflow.end_run()
    with mlflow.start_run() as run:
        mlflow.log_param("description", run_desc)
        mlflow.log_param("data_version", settings.get("training_data", "df_data_all_cleaned.csv"))
        mlflow.log_param("random_state", settings.get("train_seed", 42))
        mlflow.log_param("previous_run_id", model_id if model_id else "None")
        mlflow.log_metric("loss", loss)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("epochs", epochs)

        logger.info(f"Tentative de log du modèle dans MLflow avec artifact_path={artifact_path}")
        try:
            import sklearn.base
            if isinstance(model, sklearn.base.BaseEstimator):
                mlflow.sklearn.log_model(model, artifact_path)
                logger.info("Modèle sklearn loggé avec mlflow.sklearn.log_model.")
            else:
                import tensorflow as tf
                if isinstance(model, tf.keras.Model):
                    mlflow.keras.log_model(model, artifact_path)
                    logger.info("Modèle keras loggé avec mlflow.keras.log_model.")
                else:
                    logger.error(f"Type de modèle non supporté pour le log MLflow: {type(model)}")
        except Exception as e:
            logger.error(f"Erreur lors du log du modèle dans MLflow: {e}")
        logger.info(f"Run {run_idx + 1} completed, run_id={run.info.run_id}")
        
        # Sauvegarde des informations d'entraînement dans un fichier
        MLFlow_backup_train_infos(run_idx, run.info.run_id, hist, model, model_id, X_test, y_test)

        return run.info.run_id

def MLFlow_backup_train_infos(run_idx, run_id, hist, model, model_id, X_test, y_test):
    """
    Sauvegarde les informations d'entraînement du modèle dans des fichiers.
    """
    # step_base_name = f"model_{today_str}_{run_idx}_{model_id}"
    step_base_name = f"model_{today_str}_{run_idx}_{run_id}"
    
    model_save_settings = {
        "save_model": settings.get("save_model", True),  # should be False when tests are finished
        "save_cost": settings.get("save_cost", True),    # should be False when tests are finished
        "step_base_name": step_base_name,
        "step": run_idx
    }
    
    
     # Prédictions et matrice de confusion
    preds = model.predict(X_test)
    y_pred = preds.argmax(axis=1)
    y_true = y_test.argmax(axis=1)
    
    cm = confusion_matrix(y_true, y_pred)
    # Options de sauvegarde model et cost picture
    step_base_name = model_save_settings.get("step_base_name", f"model_{today_str}_ml_{model_save_settings.get('step', 'default')}")
    if model_save_settings.get("save_model", True):
        joblib.dump(model, join('models', f'{step_base_name}.pkl'))
        logger.info(f"Model saved as {step_base_name}.pkl")
    if model_save_settings.get("save_cost", True):
        draw_loss(hist, cm, join('figures',f'{step_base_name}.jpg'))
    
    
def MLFlow_Transmit_weights(model_new, run_id, artifact_path="linear_regression_model"):
    """ 
    Transmet les poids d'un modèle existant à un nouveau modèle depuis MLflow.
    Args:
        model_new: Le modèle Keras dans lequel les poids seront transférés.
        run_id: L'ID du run MLflow d'où les poids seront extraits.
        artifact_path: Le chemin de l'artéfact dans MLflow où le modèle est stocké.
        Returns:
        model_uri: L'URI du modèle dans MLflow après le transfert des poids.
    """
    model_uri = f"runs:/{run_id}/{artifact_path}"
    if not mlflow.get_artifact_uri(model_uri):
        logger.error(f"Model URI {model_uri} not found in MLflow.")
        return None
    
    
    logger.info(f"Transmitting weights from model at {model_uri} to new model.")
    
    
    
    model_old = MLFlow_load_model(model_uri, artifact_path)
    
    # Transfert des poids (hors couche d'entrée)
    for layer in model_new.layers:
        try:
            old_layer = model_old.get_layer(layer.name)
            # Vérifie la compatibilité des poids
            if all([w1.shape == w2.shape for w1, w2 in zip(layer.get_weights(), old_layer.get_weights())]):
                layer.set_weights(old_layer.get_weights())
                print(f"Poids transférés pour : {layer.name}")
            else:
                print(f"Forme incompatible pour : {layer.name}, poids non transférés")
        except ValueError:
            print(f"Nouvelle couche ou nom absent : {layer.name}")
    logger.info(f"Model weights transmitted to MLflow run {run_id} at {artifact_path}.")
    return model_uri