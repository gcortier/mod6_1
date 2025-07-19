import requests
import pandas as pd
import os

def fetch_parquet(url, save_path="data/adult_all.parquet"):
    """
    Télécharge le fichier Parquet depuis l'API database et le sauvegarde localement.
    """
    resp = requests.get(url)
    if resp.status_code == 200:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(resp.content)
        return save_path
    else:
        raise Exception(f"Erreur téléchargement Parquet: {resp.status_code}")


def load_parquet(parquet_path):
    """
    Charge le fichier Parquet en DataFrame.
    """
    return pd.read_parquet(parquet_path)
