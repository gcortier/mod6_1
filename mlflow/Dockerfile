FROM python:3.10-slim

RUN pip install mlflow[extras]

EXPOSE 5000

ENTRYPOINT ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000", "--backend-store-uri", "/mlflow/mlruns", "--default-artifact-root", "/mlflow/artifacts"]
