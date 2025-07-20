# Template MLOps – FastIA

## Objectif
## Description du projet minimal

Ce projet fournit un modèle prêt à l’emploi intégrant :
- **Frontend** : Application utilisateur avec Streamlit.
- **Backend** : API développée avec FastAPI.
- **Observabilité & Analyse** : Surveillance et analyse via Loguru (logs), Prometheus (métriques), Grafana (visualisation) et Uptime Kuma (monitoring de disponibilité).
- **Tests** : Couverture unitaire avec Pytest.
- **Conteneurisation** : Orchestration complète avec Docker Compose.
- **CI/CD** : Automatisation des tests et du déploiement des images Docker grâce à GitHub Actions.

L’ensemble permet de développer, tester, surveiller et déployer rapidement une application IA moderne, tout en assurant la qualité et la disponibilité du service.

## Structure du projet

```
.
├── frontend/
│   ├── app.py           # Interface utilisateur Streamlit
│   └── Dockerfile       # Image Docker du frontend
├── backend/
│   ├── main.py          # API FastAPI (3 routes)
│   ├── modules/
│   │   └── calcul.py    # Fonction de calcul (carré)
│   ├── tests/
│   │   └── test_calcul.py # Test Pytest
│   └── Dockerfile       # Image Docker du backend
├── docker-compose.yml   # Orchestration des services
└── .github/
    └── workflows/
        └── test.yml     # CI GitHub Actions
```

## Fonctionnalités
- **Frontend** : Champ pour saisir un entier, envoi à l’API, affichage du carré.
- **Backend** :
  - `/` : Message d’accueil
  - `/health` : Vérification de santé
  - `/calcul` : Retourne le carré d’un entier (validation Pydantic)
- **Logs** : Intégration Loguru sur front et back
- **Tests** : Couverture de la fonction de calcul avec Pytest
- **CI/CD** : Lancement automatique des tests à chaque push


## Installation & Lancement
- Le `.venv` 
```bash
python -m venv .venv
```
- activer l'environnement virtuel :
```bash
.venv\Scripts\Activate.ps1
```
- Installer requierements :
```bash
pip install -r requirements.txt
```

### 1. Lancer avec Docker Compose
```bash
docker compose up --build
```
- Frontend : http://localhost:8501
- Backend : http://localhost:8000/docs

### 2. Lancer les tests backend (optionnel, hors Docker)
```bash
cd backend
pytest tests/
```

### Installation rapide (hors Docker)
```bash
pip install fastapi uvicorn loguru pydantic pytest streamlit requests prometheus-client python-multipart psutil
```
```bash
pip install -r requirements.txt
```
# sauvegarder le fichier requirements.txt
```bash
pip freeze > requirements.txt
```

# lancer les services à la main
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
streamlit run app.py --server.port=8501
```


## CI/CD sur branches main et dev
- Les tests sont lancés automatiquement via GitHub Actions (`.github/workflows/test.yml`).
- La dernière version de chaque image Docker est poussée sur Docker Hub à chaque push. (`.github/workflows/docker-publish.yml`)






## Etapes de travail
- Récupération de tout ce qui a été fait dans les autre modules pour faire un projet minimal avec fast api et streamlit, dockerisé et prêt pour l’intégration continue.
- Exploration du doc github Actions : [Github_Actions](https://docs.google.com/document/d/1EgYEtMalAhMkZm5m78RHs62w6ngZxsqZOKuqMbj2E8c/edit?tab=t.0)
- Compliqué de setup correctement les contecte d'executions.
- Phase docker build CD
- Ajout des secrets DOCKER_* dans la partie action de github
- Exploration du doc et tests pour Uptime Kuma + hook discord
- Explorations et setup à partir du projet git docker-compose-prometheus-grafana en référence + qq articles :
  - [Building a Monitoring Stack with Prometheus, Grafana, and Alerting: A Docker Compose](https://medium.com/@ravipatel.it/building-a-monitoring-stack-with-prometheus-grafana-and-alerting-a-docker-compose-ef78127e4a19)
  - Monitoring systeme avec Prometheus et Grafana (dashboard 1860) : on doit ajouter un container node-exporter pour monitorer le système
  - Ajout et visualisation du dashboard dans Grafana
    - Trouver un moyen d'automatiser les logs des appels aux routes : implementation 'prometheus-fastapi-instrumentator'
  - Ajout d'un dashboard pour visualiser les appels à l'API FastAPI
  - Mise en place Grafana + cache doker

---

# Plan de réalisation – Projet MNIST Feedback & Réentraînement

## 1. Analyse des besoins et architecture générale
- Comprendre le flux utilisateur : dessin → prédiction → correction → stockage → analyse → réentraînement.
- Définir l’architecture modulaire : frontend (Streamlit), backend (FastAPI), stockage, orchestration (Prefect), monitoring (Grafana/MLflow), optimisation (Optuna).

## 2. Interface utilisateur (Frontend)
- Développer une interface Streamlit avec st_canvas pour dessiner un chiffre.
- Conversion du dessin en image 28x28 niveaux de gris (NumPy array).
- Envoi de l’image à l’API FastAPI pour prédiction.
- Affichage du résultat et possibilité de correction (sélecteur 0-9 + bouton "Corriger").

## 3. API de prédiction (Backend)
- Créer une API FastAPI avec :
  - Route /predict : reçoit l’image, prédit la classe avec un modèle CNN MNIST, retourne la prédiction.
  - Route /correct : reçoit l’image et la correction, stocke l’exemple corrigé.
- Gérer le stockage des données corrigées (CSV ou SQLite).

## 4. Stockage et gestion des données
- Définir le format de stockage (image, label, date, correction, etc.).
- Implémenter un script de nettoyage, validation et intégration des nouvelles données.

## 5. Orchestration et automatisation (Prefect)
- Mettre en place un flow Prefect qui :
  - Analyse régulièrement les nouvelles données.
  - Détecte les classes à fort taux d’échec.
  - Déclenche le réentraînement du modèle si besoin.

## 6. Réentraînement et optimisation (Optuna)
- Script de réentraînement du modèle avec intégration des nouvelles données.
- Utilisation d’Optuna pour l’optimisation des hyperparamètres.
- Versionner les modèles, données, métriques et configurations.

## 7. Monitoring et détection de dérive
- Intégrer un tableau de bord (Grafana, MLflow, TensorBoard) pour suivre les performances.
- Mettre en place un système d’alerte en cas de dérive de performance (concept/data drift).

## 8. Documentation et livrables
- Documenter : architecture, choix techniques, pipeline, conditions de déclenchement, performances avant/après.
- Préparer le schéma de la boucle de feedback.
- Rédiger le README et livrer le projet sur GitHub.

---

## Roadmap synthétique
1. Initialisation du projet, récupération du template module 5.
2. Développement du frontend Streamlit.
3. Développement de l’API FastAPI.
4. Mise en place du stockage et scripts de gestion des données.
5. Intégration Prefect pour l’automatisation.
6. Implémentation du réentraînement et d’Optuna.
7. Mise en place du monitoring et détection de dérive.
8. Documentation, tests, CI/CD, livraison.



# EXPLORATION des entrainnements

# Entrainnement Machine Learning (RandomForest) :
{ 
  "accuracy": 0.8378437126399304,
  "f1": 0.8349649103916751,
  "duration": 7.272804498672485,
  "model_path": "models/model_rf.pkl",
  "cpu_usage": 5.28
}

## Entrainnement Deep Learning  (MLP Keras) :
{
  "accuracy": 0.8299097924138681,
  "f1": 0.8244253135301817,
  "duration": 53.182822942733765,
  "model_path": "models/model_dl.h5",
  "cpu_usage": 78.87
}




# Interprétation
## Performance :
Le modèle ML classique (RandomForest) obtient une accuracy et un F1-score légèrement supérieurs au modèle deep learning, sur ce jeu de données tabulaire.
## Temps d’entraînement :
Le RandomForest est beaucoup plus rapide (7s vs 53s) et consomme moins de ressources CPU.
Efficacité ressources :
Le ML classique est plus sobre et efficace pour ce type de données (tabulaires, peu de features complexes).
Deep Learning :
Le MLP n’apporte pas de gain de performance ici, mais consomme plus de temps et de CPU. Il serait pertinent pour des données plus complexes (images, texte…).
## Recommandation
Pour ce cas d’usage, le pipeline ML classique est à privilégier :
Meilleure performance, rapidité, sobriété.
Plus facile à monitorer et à déployer.

Le pipeline DL peut être conservé pour des tests ou des cas futurs, mais n’est pas optimal ici.


## Poids du modèle
Poids du modèle ML (RandomForest): 95.86 Mo
Poids du modèle DL (MLP Keras): 0.12 Mo


Explication de cette différence :

Le RandomForest sauvegarde la structure complète de chaque arbre (noeuds, splits, valeurs, etc.) pour des centaines d’arbres, ce qui peut devenir très volumineux si le modèle est entraîné avec beaucoup de données ou si le nombre d’arbres est élevé.
Le MLP Keras, même s’il est un réseau de neurones, reste très compact ici car il n’a que quelques couches et peu de paramètres (le jeu de données est simple et le réseau n’a pas besoin d’être profond). Les poids sont stockés sous forme de matrices, ce qui est très efficace en mémoire.



Si tu veux optimiser le poids du RandomForest, tu peux :

Réduire le nombre d’arbres (n_estimators)
Limiter la profondeur (max_depth)
Utiliser des méthodes de compression (joblib avec compress=3)