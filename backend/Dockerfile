FROM python:3.11-slim
WORKDIR /app
# RUN pip install fastapi uvicorn loguru pydantic pytest
# execure l'install depuis requierements.txt
COPY requirements.txt ./
RUN pip install -r requirements.txt
# copy selective
COPY main.py ./
COPY api_base.py ./
COPY modules ./modules
COPY tests ./tests
# Copy tout le contenu du dossier courant dans le conteneur
# COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
