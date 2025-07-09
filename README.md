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

## Modules à installer (hors Docker)

- **Backend** :
  - fastapi
  - uvicorn
  - loguru
  - pydantic
  - pytest

- **Frontend** :
  - streamlit
  - loguru
  - requests

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


## CI/CD
- Les tests sont lancés automatiquement via GitHub Actions (`.github/workflows/test.yml`).
- La dernière version de chaque image Docker est poussée sur Docker Hub à chaque push.



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

