import os
from loguru import logger
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime

# Fonction utilitaire pour configurer Loguru avec rotation et rétention des logs
def setup_loguru(logfile="logs/app.log"):
    # Crée le dossier des logs si nécessaire
    os.makedirs(os.path.dirname(logfile), exist_ok=True)
    # Supprime les handlers existants pour éviter les doublons
    logger.remove()
    # Ajoute un nouveau handler avec rotation et rétention
    logger.add(
        logfile,
        rotation="500MB",      # Fichier log tournant à 500MB
        retention="7 days",    # Conservation des logs pendant 7 jours
        level="INFO",          # Niveau de log minimum
        format="{time} {level} {message}"  # Format des logs
    )
    return logger

# Fonction de création de l'application FastAPI
def create_app():
    # Ici, on pourrait ajouter des middlewares, des routes, etc.
    return FastAPI()

# Création de l'instance FastAPI
app = create_app()

# Modèle de réponse standardisé pour l'API
class Response(BaseModel):
    response: str

# Modèle de réponse standardisé complexe
class BaseResponse(BaseModel):
    success: bool
    status: str
    data: dict
    time: str

# Route racine de l'API, pour vérifier que l'API fonctionne
@app.get("/")
async def root(request: Request):
    """
    Endpoint racine de l'API.
    Retourne un message de bienvenue : "Bienvenue sur l'API".
    Cette route est utilisée pour vérifier que l'API fonctionne correctement.
    """
    try:
        # Log l'appel à la route avec l'adresse IP du client
        logger.info(f"Route '{request.url.path}' called by {request.client.host}")
        return {"response": "Bienvenue sur l'API"}
    except Exception as e:
        # Log l'erreur et retourne une erreur HTTP 500
        logger.error(f"Error logging request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint de santé pour vérifier que l'application fonctionne
@app.get("/health", response_model=BaseResponse)
async def health(request: Request):
    """
    Endpoint de santé pour vérifier que l'application fonctionne.
    Retourne un objet structuré avec success, status, data et time.
    """
    # Log l'appel à la route de santé
    logger.info(f"Route '{request.url.path}' called by {request.client.host}")
    return {
            "success": True,
            "status": "healthy",
            "data": {"message": "API is running"},
            "time": datetime.utcnow().isoformat() + 'Z'
    }
