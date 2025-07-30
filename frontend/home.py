import streamlit as st
from PIL import Image

st.set_page_config(page_title="Accueil - Prédiction Retard de Vol", page_icon="✈️", layout="centered")

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

st.markdown("""
---
*Plateforme développée pour la supervision des opérations aéroportuaires et compagnies aériennes.*
Code with ❤️ by Fast AI

""")