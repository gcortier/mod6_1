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

## Structure du projet

```
mod_tdf/
│
├── analyse-retards-avion.ipynb   # Notebook principal d'analyse et de modélisation
├── journal-de-bord.ipynb         # Journal de bord du projet
├── README.md                     # Présentation et consignes du projet
├── .gitignore                    # Fichiers à ignorer par git
├── requirements.txt              # Dépendances Python
├── dataset/                      # Dossier source des données (à ne pas versionner)
│   └── 2016_MM.csv               # Fichier de données principal
├── Matrices/                     # Dossier pour les matrices, journaux, ou autres ressources
│   └── ...
```


Variables temporelles
- **DAY_OF_WEEK** : Jour de la semaine (1 = lundi, 7 = dimanche)
- **FL_DATE** : Date complète du vol (format AAAA-MM-JJ)

Informations sur le vol
- **UNIQUE_CARRIER** : Code unique du transporteur (ex. : 'AA' pour American Airlines)
- **AIRLINE_ID** : Identifiant numérique de la compagnie aérienne
- **CARRIER** : Code du transporteur
- **TAIL_NUM** : Numéro de queue de l'avion
- **FL_NUM** : Numéro du vol

Aéroport d'origine
- **ORIGIN_AIRPORT_ID** : Identifiant de l'aéroport d'origine
- **ORIGIN_AIRPORT_SEQ_ID** : Identifiant de séquence de l'aéroport d'origine
- **ORIGIN_CITY_MARKET_ID** : Identifiant du marché de la ville d'origine
- **ORIGIN** : Code IATA de l'aéroport d'origine (ex. : 'JFK')
- **ORIGIN_CITY_NAME** : Nom de la ville d'origine
- **ORIGIN_STATE_ABR** : Abréviation de l'État d'origine
- **ORIGIN_STATE_FIPS** : Code FIPS de l'État d'origine
- **ORIGIN_STATE_NM** : Nom complet de l'État d'origine
- **ORIGIN_WAC** : Code de zone de l'aéroport d'origine

Aéroport de destination
- **DEST_AIRPORT_ID** : Identifiant de l'aéroport de destination
- **DEST_AIRPORT_SEQ_ID** : Identifiant de séquence de l'aéroport de destination
- **DEST_CITY_MARKET_ID** : Identifiant du marché de la ville de destination
- **DEST** : Code IATA de l'aéroport de destination
- **DEST_CITY_NAME** : Nom de la ville de destination
- **DEST_STATE_ABR** : Abréviation de l'État de destination
- **DEST_STATE_FIPS** : Code FIPS de l'État de destination
- **DEST_STATE_NM** : Nom complet de l'État de destination
- **DEST_WAC** : Code de zone de l'aéroport de destination

Horaires et retards
- **CRS_DEP_TIME** : Heure de départ prévue (au format HHMM)
- **DEP_TIME** : Heure réelle de départ
- **DEP_DELAY** : Retard au départ en minutes (négatif si en avance)
- **DEP_DELAY_NEW** : Retard au départ, avec 0 pour les retards ≤ 0
- **DEP_DEL15** : Indicateur de retard au départ ≥ 15 minutes (1 = oui, 0 = non)
- **DEP_DELAY_GROUP** : Groupe de retard au départ (par tranches de 15 minutes)
- **DEP_TIME_BLK** : Plage horaire du départ (ex. : '0600-0659')
- **TAXI_OUT** : Temps de roulage avant le décollage (en minutes)
- **WHEELS_OFF** : Heure de décollage (roues quittant le sol)
- **WHEELS_ON** : Heure d'atterrissage (roues touchant le sol)
- **TAXI_IN** : Temps de roulage après l'atterrissage (en minutes)
- **CRS_ARR_TIME** : Heure d'arrivée prévue
- **ARR_TIME** : Heure réelle d'arrivée
- **ARR_DELAY** : Retard à l'arrivée en minutes
- **ARR_DELAY_NEW** : Retard à l'arrivée, avec 0 pour les retards ≤ 0
- **ARR_DEL15** : Indicateur de retard à l'arrivée ≥ 15 minutes (1 = oui, 0 = non)
- **ARR_DELAY_GROUP** : Groupe de retard à l'arrivée (par tranches de 15 minutes)
- **ARR_TIME_BLK** : Plage horaire de l'arrivée (ex. : '0900-0959')

Annulations et détournements
- **CANCELLED** : Indicateur d'annulation du vol (1 = oui, 0 = non)
- **CANCELLATION_CODE** : Code de la raison de l'annulation (A = transporteur, B = météo, C =NAS, D = sécurité)
- **DIVERTED** : Indicateur de vol détourné (1 = oui, 0 = non)

Durées et distances
- **CRS_ELAPSED_TIME** : Durée prévue du vol (en minutes)
- **ACTUAL_ELAPSED_TIME** : Durée réelle du vol (en minutes)
- **AIR_TIME** : Temps de vol effectif (en minutes)


# Aperçu des colonnes
Index(['YEAR', 'QUARTER', 'MONTH', 'DAY_OF_MONTH', 'DAY_OF_WEEK', 'FL_DATE',
       'UNIQUE_CARRIER', 'AIRLINE_ID', 'CARRIER', 'TAIL_NUM', 'FL_NUM',
       'ORIGIN_AIRPORT_ID', 'ORIGIN_AIRPORT_SEQ_ID', 'ORIGIN_CITY_MARKET_ID',
       'ORIGIN', 'ORIGIN_CITY_NAME', 'ORIGIN_STATE_ABR', 'ORIGIN_STATE_FIPS',
       'ORIGIN_STATE_NM', 'ORIGIN_WAC', 'DEST_AIRPORT_ID',
       'DEST_AIRPORT_SEQ_ID', 'DEST_CITY_MARKET_ID', 'DEST', 'DEST_CITY_NAME',
       'DEST_STATE_ABR', 'DEST_STATE_FIPS', 'DEST_STATE_NM', 'DEST_WAC',
       'CRS_DEP_TIME', 'DEP_TIME', 'DEP_DELAY', 'DEP_DELAY_NEW', 'DEP_DEL15',
       'DEP_DELAY_GROUP', 'DEP_TIME_BLK', 'TAXI_OUT', 'WHEELS_OFF',
       'WHEELS_ON', 'TAXI_IN', 'CRS_ARR_TIME', 'ARR_TIME', 'ARR_DELAY',
       'ARR_DELAY_NEW', 'ARR_DEL15', 'ARR_DELAY_GROUP', 'ARR_TIME_BLK',
       'CANCELLED', 'CANCELLATION_CODE', 'DIVERTED', 'CRS_ELAPSED_TIME',
       'ACTUAL_ELAPSED_TIME', 'AIR_TIME', 'FLIGHTS', 'DISTANCE',
       'DISTANCE_GROUP', 'CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY',
       'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY', 'FIRST_DEP_TIME',
       'TOTAL_ADD_GTIME', 'LONGEST_ADD_GTIME', 'Unnamed: 64'],
      dtype='object')


# Probleme de doublons
2% de doublions dans le dataset


Nettoyage/ normalisation : 
- On vire les lignes :
- avec la valeur cible manquant : ARR_DEL15
- on vire les colonnnes:
- FLIGHTS (1 seule valeur donc inutile)

On rempli avec des valeurs 0
CARRIER_DELAY, WEATHER_DELAY, NAS_DELAY, SECURITY_DELAY, LATE_AIRCRAFT_DELAY, TOTAL_ADD_GTIME, LONGEST_ADD_GTIME, 

# a trancher 
FIRST_DEP_TIME




https://www.kaggle.com/datasets/usdot/flight-delays


https://www.kaggle.com/code/fabiendaniel/predicting-flight-delays-tutorial
https://www.kaggle.com/code/manasichhibber/flight-delay-predictions/notebook