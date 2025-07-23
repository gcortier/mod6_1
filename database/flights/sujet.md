# Sujet Examen : Prédiction des retards d’avion

## Introduction
Les retards de vols constituent une problématique majeure dans le secteur aérien, impactant passagers, compagnies aériennes et aéroports. En 2019, environ 19 % des vols ont été retardés aux États-Unis, engendrant des coûts économiques estimés à 28 milliards de dollars.

Les retards peuvent entraîner :
- Correspondances manquées
- Insatisfaction des clients
- Perturbations opérationnelles

Ils résultent de divers facteurs :
- Conditions météorologiques
- Congestion du trafic aérien
- Problèmes techniques ou opérationnels

Face à cette complexité, l’analyse prédictive devient essentielle pour anticiper et gérer efficacement les retards. Ces techniques permettent d’analyser des données historiques (et potentiellement en temps réel) pour :
- Identifier les causes des retards
- Estimer leur probabilité et leur durée
- Optimiser les décisions opérationnelles

Le Bureau of Transportation Statistics (BTS) des États-Unis a mis à disposition un jeu de données pour démontrer comment le machine learning peut anticiper les retards de vols, améliorer la satisfaction des passagers et optimiser les opérations.

**Objectif principal** : Développer un modèle de classification capable de prédire si un vol sera retardé de plus de 15 minutes à l’arrivée (prédiction binaire : retardé ou non).

---

## Sujet
Construire et déployer un modèle capable d’effectuer une prédiction des retards d’avion.

En tant que professionnel de la Data, vous devrez :
- Maintenir l’infrastructure nécessaire au déploiement continu d’un modèle de prédiction de retards de vols
- Industrialiser le processus d’ETL pour la préparation des données
- Prendre en compte les risques, menaces, aspects éthiques et légaux lors du stockage et de l’exploitation des données
- Anticiper l’historisation des données, notamment des retards
- Documenter chaque étape de construction du modèle relationnel (tables de faits et de dimensions, modèle relationnel, optimisation pour la montée en charge)
- Utiliser et paramétrer un algorithme d’IA adapté à la problématique

---

## Jeu de données à disposition
Le jeu de données fourni par le BTS contient plusieurs fichiers (1 par mois).

### Variables temporelles
- **DAY_OF_WEEK** : Jour de la semaine (1 = lundi, 7 = dimanche)
- **FL_DATE** : Date complète du vol (AAAA-MM-JJ)

### Informations sur le vol
- **UNIQUE_CARRIER** : Code unique du transporteur (ex. : 'AA')
- **AIRLINE_ID** : Identifiant numérique de la compagnie
- **CARRIER** : Code du transporteur
- **TAIL_NUM** : Numéro de queue de l’avion
- **FL_NUM** : Numéro du vol

### Aéroport d’origine
- **ORIGIN_AIRPORT_ID**
- **ORIGIN_AIRPORT_SEQ_ID**
- **ORIGIN_CITY_MARKET_ID**
- **ORIGIN** : Code IATA (ex. : 'JFK')
- **ORIGIN_CITY_NAME**
- **ORIGIN_STATE_ABR**
- **ORIGIN_STATE_FIPS**
- **ORIGIN_STATE_NM**
- **ORIGIN_WAC**

### Aéroport de destination
- **DEST_AIRPORT_ID**
- **DEST_AIRPORT_SEQ_ID**
- **DEST_CITY_MARKET_ID**
- **DEST** : Code IATA
- **DEST_CITY_NAME**
- **DEST_STATE_ABR**
- **DEST_STATE_FIPS**
- **DEST_STATE_NM**
- **DEST_WAC**

### Horaires et retards
- **CRS_DEP_TIME** : Heure de départ prévue (HHMM)
- **DEP_TIME** : Heure réelle de départ
- **DEP_DELAY** : Retard au départ (min)
- **DEP_DELAY_NEW** : Retard au départ, 0 si ≤ 0
- **DEP_DEL15** : Retard au départ ≥ 15 min (1 = oui, 0 = non)
- **DEP_DELAY_GROUP** : Groupe de retard au départ (tranches de 15 min)
- **DEP_TIME_BLK** : Plage horaire du départ
- **TAXI_OUT** : Temps de roulage avant décollage (min)
- **WHEELS_OFF** : Heure de décollage
- **WHEELS_ON** : Heure d’atterrissage
- **TAXI_IN** : Temps de roulage après atterrissage (min)
- **CRS_ARR_TIME** : Heure d’arrivée prévue
- **ARR_TIME** : Heure réelle d’arrivée
- **ARR_DELAY** : Retard à l’arrivée (min)
- **ARR_DELAY_NEW** : Retard à l’arrivée, 0 si ≤ 0
- **ARR_DEL15** : Retard à l’arrivée ≥ 15 min (1 = oui, 0 = non)
- **ARR_DELAY_GROUP** : Groupe de retard à l’arrivée (tranches de 15 min)
- **ARR_TIME_BLK** : Plage horaire de l’arrivée

### Annulations et détournements
- **CANCELLED** : Vol annulé (1 = oui, 0 = non)
- **CANCELLATION_CODE** : Raison de l’annulation (A = transporteur, B = météo, C = NAS, D = sécurité)
- **DIVERTED** : Vol détourné (1 = oui, 0 = non)

### Durées et distances
- **CRS_ELAPSED_TIME** : Durée prévue du vol (min)
- **ACTUAL_ELAPSED_TIME** : Durée réelle du vol (min)
- **AIR_TIME** : Temps de vol effectif (min)

---

## Compétences à démontrer
- **C1.** Identifier un jeu de données pertinent
- **C2.** Identifier les risques éthiques et sociétaux
- **C3.** Préparer les données pour renforcer leur intégrité et pertinence
- **C4.** Choisir un modèle IA adapté et performant
- **C5.** Entraîner le modèle d’IA de façon automatique et supervisée
- **C6.** Implémenter le modèle d’IA dans l’environnement technique
- **C8.** Mesurer la performance et les impacts de la solution d’IA
- **C9.** Adopter une démarche d’amélioration continue