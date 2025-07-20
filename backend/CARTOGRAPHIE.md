# Cartographie du service backend

backend/
├── main.py                # API FastAPI (routes de prédiction, correction, calcul, etc.)
├── training/
│   ├── train.py           # Script principal pour entraîner le modèle
│   ├── preprocess.py      # Fonctions de prétraitement des données
│   ├── model.py           # Définition et sauvegarde du modèle (sklearn, keras, etc.)
│   └── evaluate.py        # Évaluation du modèle (métriques, logs)
├── utils/
│   └── fetch_data.py      # Fonction pour télécharger et lire le fichier Parquet
├── models/                # Dossier pour stocker les modèles entraînés
├── requirements.txt
└── Dockerfile
