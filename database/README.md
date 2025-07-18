Dans cette situation professionnelle, vous analyserez une solution IA existante de classification socio-économique afin d’en proposer une évolution architecturale. 
Votre mission est d’identifier les limites techniques, éthiques et écologiques du système, puis de concevoir une nouvelle version plus responsable. 
Vous comparerez notamment plusieurs architectures d’entraînement et d’inférence sur la base de leurs performances mais aussi de leur empreinte écologique (temps de calcul, consommation CPU/RAM).
Référentiels
Compétences transversales
[Atlas IA] Concevoir et implémenter une solution d'IA
Compétences visées
Ressources
datasource
Contexte du projet
Un client de FastIA déploie depuis plusieurs années un modèle de classification basé sur des données personnelles (revenus, sexe, origine, etc.) afin de cibler des clients pour ses offres de services.

Les données utilisées sont stockées dans un fichier CSV et n'offre aucune scalabilité à grande échelle.

Ce système montre aujourd’hui plusieurs limites :

​

Son architecture est rigide et peu documentée.
Il présente un risque de discrimination algorithmique.
Il consomme trop de ressources en production, au regard de ses performances.
L’entreprise souhaite donc moderniser cette IA, la rendre plus éthique, plus sobre, et documenter son fonctionnement de bout en bout.
​

Vous devez proposer une architecture cible en analysant les compromis entre précision, coûts de calcul, soutenabilité, et acceptabilité sociale :

​

Analyser l’architecture actuelle : flux de données, composants IA, stockage, interfaces, outils d’orchestration et de monitoring.
Documenter le cycle de vie de la donnée (depuis sa collecte jusqu’à son exploitation).
Étudier les contraintes éthiques et réglementaires associées à l’architecture (biais, confidentialité, usage des données sensibles).
Évaluer la conformité aux bonnes pratiques : modularité, scalabilité, résilience, écoconception.
Formuler des recommandations d’évolution en tenant compte des objectifs métier, des performances attendues, du contexte de production et des parties prenantes.
Proposer des alternatives techniques ou de nouveaux services d’infrastructure (ex. : changement de cloud provider, refonte des pipelines, simplification des flux de données).
(Bonus-Fiction) Présenter une version documentée de l’architecture cible (diagramme, contraintes, services, budget estimé, choix justifiés).
​

Pour améliorer l'architecture et la scalabilité/maintenabilité du service vous devrez également concevoir deux services API distincts, chacun conteneurisé et isolé pour respecter les bonnes pratiques de sécurité, de modularité et de traçabilité.

​

La première API gérera l’accès à une base de données relationnelle conçue à partir d’un modèle Merise.

Cette base contiendra deux types d’informations essentielles : d’une part, les données utilisées pour l’entraînement et la prédiction (datas, entrées utilisateurs, résultats), et d’autre part, les indicateurs de performance et de consommation collectés sur les différents modèles (temps de calcul, mémoire utilisée, consommation CPU/GPU, précision, F1-score, etc.).

Cette API devra être déployée sur un réseau sécurisé, interne au cluster, sans exposition publique et sa santé devra être vérifier.

​

La seconde API, dédiée au modèle d’intelligence artificielle, sera responsable du traitement prédictif et sera complètement monitorée.

Elle exposera une interface REST sécurisée pour le front ou les clients externes, et s’appuiera sur l’API de base de données pour enregistrer ou consulter les données historiques.

Ce découpage illustre une architecture orientée microservices, où chaque brique respecte le principe de responsabilité unique tout en assurant une communication cohérente et sécurisée dans l’écosystème global.

Modalités pédagogiques
Ce travail sera mené individuellement, en plusieurs étapes :

Audit technique et éthique d’un modèle existant (Adult dataset – prédiction de revenu).
Création de plusieurs pipelines alternatifs (ex : machine learning, reseau de neurones).
Mise en place d’un suivi de consommation des ressources via Prometheus (exportateur Node ou Python) connecté à Grafana, afin de comparer les architectures sur leurs performances ET leur consommation réelle.
Documentation des choix et production d’un diagramme d’architecture cible.
Réflexion autour des enjeux éthiques, réglementaires (RGPD) et écologiques (empreinte carbone, sobriété numérique).
​

Les indicateurs que vous pouvez suivre (exemple):

CPU usage (%)
Temps d'execution de l'entrainement et de la prediction
GPU usage (%)
etc...
​

Pour vous donner une idée comparez ces valeurs au coups d'entraînement de ChatGPT.

Informez le Data Protection Officer, dont le rôle consiste à piloter la conformité au règlement européen sur la protection des données, que les choix fait en 1994 ne sont plus valable en >2025 en lui expliquant quelle donnée est accéssible aujourd'hui.

Modalités d'évaluation
Clarté de l’analyse éthique, technique et sociétale
Qualité de la documentation du cycle de la donnée
Pertinence des choix d’architecture proposés
Déploiement fonctionnel de l’architecture cible
Présentation orale claire et argumentée (facultative selon modalités)
Livrables
Audit de l’architecture actuelle (PDF ou Markdown)
Nouveau pipeline codé, versionné sur GitHub
Dashboard de monitoring
Documentation du cycle de vie des données et des risques éthiques
Présentation orale (optionnel)
Critères de performance
Le nouveau modèle est éthique
Le modèle choisi consomme moins de ressource que le précédent
Assignation
Ce brief vous a été assigné.
Lisez attentivement votre brief avant de débuter votre travail !




Suggestion d'architecture : 
```
scalable_model/               # Racine du projet ML scalable
│
├── data/                     # Répertoire pour gérer les données du projet
│   ├── raw/                  # Données brutes non modifiées (CSV initiaux, etc.)
│   └── processed/            # Données nettoyées et transformées prêtes pour l'entraînement
│
├── notebooks/                # Notebooks Jupyter pour exploration et prototypage
│
├── api/                      # Répertoire pour l'API FastAPI (prédiction)
│   ├── main.py               # Entrypoint de l’API REST pour servir le modèle
│   ├── model_loader.py       # Charger le modèle entraîné pour la prédiction
│   ├── requirements.txt      # Dépendances spécifiques à l'API FastAPI
│   └── Dockerfile            # Image Docker pour conteneuriser l’API de prédiction
│
│   ├── training/             # Pipeline d'entraînement ML pour l'API FastAPI
│   │   ├── train.py          # Script principal pour entraîner le modèle
│   │   ├── preprocess.py     # Script pour prétraiter/transformer les données
│   │   ├── evaluate.py       # Évaluer les performances du modèle entraîné
│   │   └── model.py          # Définition de l'architecture et sauvegarde du modèle
│
├── database/                 # Microservice pour gérer la base de données et migrations
│   ├── models/               # Dossier pour les modèles de données SQLAlchemy
│   │   ├── __init__.py       # Fichier d'initialisation du module schema
│   │   └── user_schema.py    # Exemple de schéma Pydantic pour les utilisateurs
│   ├── schemas/              # Dossier pour les schémas Pydantic
│   │   ├── __init__.py       # Fichier d'initialisation du module schema
│   │   └── user_schema.py    # Exemple de schéma Pydantic pour les utilisateurs
│   ├── crud/                 # Fonctions CRUD (Create, Read, Update, Delete)
│   ├── database.py           # Création de la session DB, moteur SQLAlchemy
│   ├── main.py               # Entrypoint FastAPI pour exposer l’API interne de la BDD
│   ├── alembic.ini           # Fichier de configuration Alembic
│   ├── migrations/           # Scripts de migration générés par Alembic
│   ├── alembic/              # Répertoire pour `env.py` et `versions/` Alembic
│   ├── requirements.txt      # Dépendances spécifiques au service DB
│   └── Dockerfile            # Image Docker pour conteneuriser l’API BDD + migrations
│
│   └── modules/              # Dossier pour les modules liés à la gestion de la DB
│   │   ├── __init__.py       # Fichier d'initialisation du module schema
│   │   └── db_helpers.py    # Exemple de schéma Pydantic pour les utilisateurs
|
├── monitoring/               # Configuration pour le monitoring avec Kuma, Prometheus & Grafana
│   ├── kuma/                 # Configs spécifiques à Kuma pour collecter des métriques
│   │   ├── kuma_config.yml   # Configuration principale pour Kuma
│   │   └── kuma_agent.yml    # Agent Kuma à déployer dans chaque service pour collecter les métriques
│   ├── prometheus/           # Config de Prometheus pour scraper les métriques
│   │   └── prometheus.yml    # Fichier de configuration de Prometheus pour scraper Kuma
│   ├── grafana/              # Configs Grafana : dashboards et datasources
│   │   ├── dashboards/       # Définition des dashboards Grafana
│   │   │   ├── dashboards.yml  # Fichier d'import pour dashboards
│   │   │   └── system-dashboard.yml # Exemple de dashboard système
│   │   ├── datasources/      # Config datasources Grafana (Prometheus, DB, etc.)
│   │   │   └── datasource.yml # Définition des connexions datasources
│   └── Dockerfile            # Image Docker pour conteneuriser les services de monitoring
│
├── mlruns/                   # Dossier pour stocker les artefacts modèles versionnés via MLflow
│   ├── model_v1/             # Version 1 du modèle sauvegardée (fichiers MLflow)
│   └── model_v2/             # Version 2 du modèle (itération améliorée)
│
├── tests/                    # Tests unitaires et tests end-to-end
│   ├── test_training.py      # Tests pour vérifier le pipeline d'entraînement
│   ├── test_api.py           # Tests pour l'API de prédiction (routes, réponse)
│   ├── test_db.py            # Tests pour l'API BDD (CRUD, connexion)
│   └── test_monitoring.py    # Tests basiques du monitoring (endpoint Kuma)
│
├── docker-compose.yml        # Orchestration multi-conteneurs (API, DB, monitoring)
├── Makefile                  # Commandes utiles : lint, test, build, format, etc.
├── requirements.txt          # Dépendances globales pour tout le projet
├── .env                      # Variables d'environnement (ex. : URL DB, secrets)
├── .gitignore                # Fichiers/dossiers à ignorer dans le versioning Git
└── README.md                 # Documentation principale : usage, architecture, setup
```