FROM python:3.11-slim
WORKDIR /app
# RUN pip install fastapi uvicorn loguru pydantic pytest
# execure l'install depuis requierements.txt
RUN apt-get update && apt-get install -y libgomp1
COPY requirements.txt ./
RUN pip install -r requirements.txt
# copy selective
COPY data ./data
COPY logs ./logs
# COPY figures ./figures
COPY models ./models
COPY modules ./modules
COPY training ./training
COPY utils ./utils
COPY settings ./settings
COPY tests ./tests
COPY api_base.py ./
COPY api_mlflow.py ./
COPY main.py ./
# Copy tout le contenu du dossier courant dans le conteneur
# COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
