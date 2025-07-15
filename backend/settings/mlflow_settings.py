# Fichier utilitaire pour partager les variables entre alchemy_api.py et mlflow_utils.py

settings = {
    # source de données de l'entrainnement : Original
    "source_data": "mnist_full.csv",
    # source de données de l'entrainnement : Cleaned
    "training_data": "mnist_full.csv",
    "wanted_train_cycle": 1,
    "epochs": 5,
    "batch_size": 32,
    "train_seed": 42,
    # "transfert_weights": {
    #     "active": True,  # Indique si le transfert de poids est activé
    #     "run_id": "0eceb24c95c94737a29e6b50b848b0c2"  # URI du modèle à partir duquel les poids seront transférés
    # }  
}

wanted_train_cycle = settings.get("wanted_train_cycle", 1)
artifact_path = "mnist_model"
