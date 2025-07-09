import os
import streamlit as st
from loguru import logger
import requests
from streamlit_drawable_canvas import st_canvas
import numpy as np
from PIL import Image
import io

st.title("Calculateur de carré")

API_URL = os.getenv("API_URL", "http://localhost:8000")
# API_URL = "http://localhost:8042"
st.write(f"Valeur de API_URL : : {API_URL}")
log_file = "logs/app.log"
# Configuration de Loguru pour sauvegarder les logs
logger.add(log_file, rotation="10 MB", retention="7 days", level="INFO")


# number = st.number_input("Entrez un entier", step=1, format="%d")
# if st.button("Calculer le carré"):
#     try:
#         st.write(f"Envoi de la requête à l'API : {API_URL}/calcul avec le nombre {int(number)}")
#         response = requests.post(f"{API_URL}/calcul", json={"number": int(number)})
#         if response.status_code == 200:
#             result = response.json()["result"]
#             st.success(f"Le carré de {int(number)} est {result}")
#             logger.info(f"Calcul du carré de {int(number)}: {result}")
#         else:
#             st.error(f"Erreur: {response.text}")
#             logger.error(f"Erreur API: {response.text}")
#     except Exception as e:
#         st.error(f"Erreur: {e}")
#         logger.error(f"Exception: {e}")

st.title("Data Sender")

choices = ["Red", "Blue", "Green", "Yellow"]
selected_data = st.selectbox("Choose a data", choices)

if st.button("Send Data"):
    logger.info(f"Sent data: {selected_data}")
    try:
        response = requests.post(f"{API_URL}/data", data={"data": selected_data})
        st.write(response.json())
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending data: {selected_data}")
        st.error(f"Error: {e}")

st.title("API Reconnaissance de chiffres manuscrits (MNIST)")

st.write("Dessinez un chiffre (0-9) ci-dessous :")
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 1)",
    stroke_width=10,
    stroke_color="#000000",
    background_color="#FFFFFF",
    width=280,
    height=280,
    drawing_mode="freedraw",
    key="canvas",
)

if canvas_result.image_data is not None:
    img = Image.fromarray((canvas_result.image_data).astype("uint8"), "RGBA")
    img = img.convert("L")
    img = img.resize((28, 28))
    img_array = np.array(img)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()
    st.image(img, caption="Votre chiffre (28x28)", width=100)
    if 'last_pred' not in st.session_state:
        st.session_state['last_pred'] = None
    if 'last_img_bytes' not in st.session_state:
        st.session_state['last_img_bytes'] = None

    if st.button("Prédire"):
        files = {"file": ("canvas.png", img_bytes, "image/png")}
        response = requests.post(f"{API_URL}/predict", files=files)
        logger.info(f"Envoi de l'image pour prédiction à l'API : {API_URL}/predict")
        if response.ok:
            pred = response.json()["prediction"]
            st.success(f"Prédiction du modèle : {pred}")
            st.session_state['last_pred'] = pred
            st.session_state['last_img_bytes'] = img_bytes
        else:
            st.error("Erreur lors de la prédiction.")
            st.session_state['last_pred'] = None
            st.session_state['last_img_bytes'] = None

    # Afficher la correction si une prédiction a été faite
    if st.session_state['last_pred'] is not None and st.session_state['last_img_bytes'] is not None:
        correction = st.selectbox("Corriger la prédiction si besoin :", list(range(10)), index=st.session_state['last_pred'], key="correction_select")
        if st.button("Envoyer la correction"):
            data = {"correction": correction}
            files = {"file": ("canvas.png", st.session_state['last_img_bytes'], "image/png")}
            logger.info(f"Envoi de l'image pour correction à l'API : {data}")
            r = requests.post(f"{API_URL}/correct", data=data, files=files)
            if r.ok:
                st.success("Correction enregistrée !")
            else:
                st.error("Erreur lors de l'enregistrement.")

