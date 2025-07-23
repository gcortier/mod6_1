# Brief de Référence IA – Prédiction des Retards d’Avion

## 1. Plan d’Action pour Répondre au Sujet

### 1.1. Compréhension et cadrage
- Lire et comprendre le sujet, les enjeux et les attentes métier
- Analyser le jeu de données fourni (structure, volume, variables)
- Identifier les risques éthiques, légaux et de sécurité liés aux données

### 1.2. Préparation des données (ETL)
- Collecter et agréger les fichiers mensuels
- Nettoyer les données (valeurs manquantes, doublons, incohérences)
- Sélectionner les variables pertinentes pour la prédiction
- Créer les variables cibles (retard à l’arrivée ≥ 15 min)
- Historiser les données pour permettre un suivi dans le temps

### 1.3. Modélisation et expérimentation
- Analyser les variables explicatives (corrélations, importance)
- Choisir un ou plusieurs algorithmes de classification (ex : Random Forest, XGBoost, Logistic Regression)
- Mettre en place une validation croisée et des métriques adaptées (accuracy, recall, precision, F1, ROC-AUC)
- Optimiser les hyperparamètres

### 1.4. Déploiement et industrialisation
- Industrialiser le pipeline ETL (script, notebook, ou outil dédié)
- Déployer le modèle (API, batch, ou autre)
- Mettre en place le monitoring des performances et des dérives
- Documenter chaque étape (modèle relationnel, choix techniques, etc.)

### 1.5. Suivi et amélioration continue
- Mettre à jour le modèle et les données régulièrement
- Adapter le pipeline aux évolutions des besoins et des données

---

## 2. Analyse des Colonnes du Dataset

### 2.1. Colonnes Utiles pour la Prédiction
- **DAY_OF_WEEK** : Influence potentielle sur les retards (week-end vs semaine)
- **FL_DATE** : Pour l’historisation, la saisonnalité
- **UNIQUE_CARRIER, AIRLINE_ID, CARRIER** : Identifier la compagnie (certaines compagnies plus sujettes aux retards)
- **FL_NUM** : Numéro de vol (peut être utile pour des patterns récurrents)
- **ORIGIN, DEST** : Codes IATA des aéroports (origine/destination)
- **CRS_DEP_TIME, CRS_ARR_TIME** : Heures prévues (influence sur la congestion)
- **DEP_DELAY, DEP_DELAY_NEW, DEP_DEL15** : Retard au départ (prédicteur fort du retard à l’arrivée)
- **TAXI_OUT, TAXI_IN** : Temps de roulage (peut indiquer des problèmes d’aéroport)
- **CANCELLED, DIVERTED** : Pour filtrer les vols annulés/détournés
- **CRS_ELAPSED_TIME** : Durée prévue du vol

### 2.2. Colonnes à Écarter ou à Justifier
- **TAIL_NUM** : Numéro de queue de l’avion (peu pertinent sauf analyse très fine)
- **ORIGIN_AIRPORT_ID, ORIGIN_AIRPORT_SEQ_ID, ORIGIN_CITY_MARKET_ID, ORIGIN_CITY_NAME, ORIGIN_STATE_ABR, ORIGIN_STATE_FIPS, ORIGIN_STATE_NM, ORIGIN_WAC** : Redondant avec le code IATA (ORIGIN)
- **DEST_AIRPORT_ID, DEST_AIRPORT_SEQ_ID, DEST_CITY_MARKET_ID, DEST_CITY_NAME, DEST_STATE_ABR, DEST_STATE_FIPS, DEST_STATE_NM, DEST_WAC** : Redondant avec le code IATA (DEST)
- **DEP_TIME, ARR_TIME, WHEELS_OFF, WHEELS_ON, ACTUAL_ELAPSED_TIME, AIR_TIME** : Variables postérieures à l’événement à prédire (fuites de données)
- **CANCELLATION_CODE** : Seulement utile si CANCELLED = 1
- **DEP_DELAY_GROUP, ARR_DELAY_GROUP, DEP_TIME_BLK, ARR_TIME_BLK** : Variables dérivées, à utiliser avec précaution

### 2.3. Variable Cible
- **ARR_DEL15** : Retard à l’arrivée ≥ 15 min (1 = oui, 0 = non)

---

## 3. Points de Vigilance
- Éviter les fuites de données (ne pas utiliser de variables connues après le départ)
- Prendre en compte les biais potentiels (compagnie, saison, aéroport)
- Documenter toutes les étapes pour assurer la reproductibilité et la conformité

---

**Ce brief servira de référence pour toutes les étapes du projet.**
