import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Prédiction Retard de Vol", page_icon="✈️", layout="centered")
st.title("Prédiction Retard de Vol")

# Bandeau visuel style compagnie aérienne/aéroport
st.markdown("""
    <div style='background: linear-gradient(90deg, #005baa 0%, #00c6fb 100%); padding: 2rem; border-radius: 12px; text-align: center;'>
        <h1 style='color: white; font-size: 2.5rem; margin-bottom: 0.5rem;'>AeroPredict</h1>
        <h2 style='color: #e3e3e3; font-size: 1.2rem;'>Prédiction des retards de vols en temps réel</h2>
        <img src='https://img.icons8.com/ios-filled/100/ffffff/airport.png' style='margin-top: 1rem;' alt='Airport Icon'/>
    </div>
    """, unsafe_allow_html=True)

st.write("""
Bienvenue sur la plateforme AeroPredict !

- **Objectif** : Prédire le risque de retard à l'arrivée d'un vol à partir de ses caractéristiques.
- **Fonctionnalités** :
    - Saisie interactive des données vol
    - Prédiction instantanée via IA
    - Visualisation des résultats
    - Monitoring et supervision intégrés

Cliquez sur l'onglet "Prédiction" pour tester le modèle sur vos propres données de vol.
""")



st.write("Saisissez les caractéristiques du vol pour obtenir une prédiction du retard à l'arrivée (ARR_DEL15).")

# Formulaire de saisie des features
with st.form("prediction_form"):
    day_of_week = st.number_input("Jour de la semaine (1=lundi, 7=dimanche)", min_value=1, max_value=7, value=1)
    fl_date = st.date_input("Date du vol")
    # Valeurs acceptables extraites de unique_values.md
    unique_carrier_options = ["WN", "DL", "AA", "OO", "UA", "EV", "B6", "AS", "NK", "F9", "HA", "VX"]
    origin_options = ["ATL", "ORD", "DEN", "LAX", "DFW", "SFO", "PHX", "LAS", "IAH", "SEA", "MSP", "DTW", "MCO", "BOS", "EWR", "SLC", "CLT", "BWI", "JFK", "LGA"]
    dest_options = ["ATL", "ORD", "DEN", "LAX", "DFW", "SFO", "PHX", "LAS", "IAH", "SEA", "MSP", "MCO", "DTW", "BOS", "SLC", "EWR", "CLT", "BWI", "LGA", "JFK"]

    unique_carrier = st.selectbox("Code compagnie (UNIQUE_CARRIER)", unique_carrier_options)
    airline_id = st.number_input("ID compagnie (AIRLINE_ID)", min_value=0)
    origin = st.selectbox("Aéroport origine (ORIGIN)", origin_options)
    dest = st.selectbox("Aéroport destination (DEST)", dest_options)
    crs_dep_time = st.number_input("Heure départ prévue (CRS_DEP_TIME, HHMM)", min_value=0)
    dep_time = st.number_input("Heure départ réelle (DEP_TIME, HHMM)", min_value=0)
    dep_delay = st.number_input("Retard au départ (DEP_DELAY, minutes)", value=0.0)
    dep_del15 = st.number_input("Retard départ >=15min (DEP_DEL15)", min_value=0, max_value=1, value=0)
    taxi_out = st.number_input("Taxi out (TAXI_OUT, minutes)", value=0.0)
    wheels_off = st.number_input("Heure décollage (WHEELS_OFF, HHMM)", min_value=0)
    crs_arr_time = st.number_input("Heure arrivée prévue (CRS_ARR_TIME, HHMM)", min_value=0)
    crs_elapsed_time = st.number_input("Durée prévue (CRS_ELAPSED_TIME, minutes)", value=0.0)
    arr_del15 = st.number_input("Retard arrivée >=15min (ARR_DEL15, optionnel)", min_value=0, max_value=1, value=0)
    submit = st.form_submit_button("Prédire")

if submit:
    # Conversion date en timestamp (secondes)
    fl_date_ts = int(datetime.datetime.combine(fl_date, datetime.time()).timestamp())
    payload = {
        "data": [{
            "DAY_OF_WEEK": day_of_week,
            "FL_DATE": fl_date_ts,
            "UNIQUE_CARRIER": unique_carrier,
            "AIRLINE_ID": airline_id,
            "ORIGIN": origin,
            "DEST": dest,
            "CRS_DEP_TIME": crs_dep_time,
            "DEP_TIME": dep_time,
            "DEP_DELAY": dep_delay,
            "DEP_DEL15": dep_del15,
            "TAXI_OUT": taxi_out,
            "WHEELS_OFF": wheels_off,
            "CRS_ARR_TIME": crs_arr_time,
            "CRS_ELAPSED_TIME": crs_elapsed_time,
            "ARR_DEL15": arr_del15
        }]
    }
    api_url = st.secrets["API_URL"] if "API_URL" in st.secrets else "http://backend:8000/predict-gbm"
    try:
        resp = requests.post(api_url, json=payload)
        resp.raise_for_status()
        result = resp.json()
        pred = result["results"][0]["prediction"]
        st.success(f"Prédiction : {'Retard' if pred == 1 else 'Pas de retard'} ({pred})")
        st.write(result)
    except Exception as e:
        st.error(f"Erreur API : {e}")



st.markdown("""
---
*Plateforme développée pour la supervision des opérations aéroportuaires et compagnies aériennes.*
Code with ❤️ by Fast AI

""")