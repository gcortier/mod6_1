# Copilot Instructions for AI Coding Agents

## Project Overview
This codebase is a modular MLOps template for deploying, monitoring, and retraining AI services. It features:
- **Frontend**: Streamlit app for user interaction and feedback.
- **Backend**: FastAPI microservices for prediction, correction, and database access.
- **Database**: MySQL with SQLAlchemy models, exposed via a dedicated FastAPI service.
- **Monitoring**: Prometheus, Grafana, and Uptime Kuma for metrics and health checks.
- **Orchestration**: Prefect for automation and MLflow for model/version tracking.
- **CI/CD**: GitHub Actions for tests and Docker image builds.

## Architecture & Data Flow
- Data flows from user input (Streamlit) → prediction (FastAPI) → correction/storage (DB/API) → monitoring (Prometheus/Grafana) → retraining (Prefect/MLflow).
- All services are containerized and orchestrated via `docker-compose.yml`. Key ports: 8000 (backend), 8011 (database API), 8501 (frontend), 3306 (MySQL).
- Database API exposes `/dataframe` for ML pipelines to fetch training data. Use pagination/filters for large datasets.

## Developer Workflows
- **Build & Run**: Use `docker compose up --build` for full stack. Individual services can be run with `uvicorn main:app --port <PORT>` or `streamlit run app.py`.
- **Testing**: Run `pytest` in backend/tests. CI runs on push via `.github/workflows/test.yml`.
- **Monitoring**: Prometheus scrapes metrics; Grafana dashboards are provisioned from `grafana_mnistretrain/provisioning`.
- **Database Init**: MySQL container auto-initializes from `database/data` scripts.

## Project-Specific Patterns
- **Microservices**: Each API (backend, database) is isolated, communicates via REST, and is monitored independently.
- **Data Access**: ML pipelines should fetch data via the database API, not direct DB queries. Use `/dataframe` endpoint, and prefer batch or paginated access.
- **Model Versioning**: Store models in `mlruns/` and track with MLflow.
- **Stat Logging**: Metrics and training stats should be POSTed to the database API for centralization.
- **Config**: Use `.env` for secrets and environment variables. Docker Compose injects these into containers.

## Integration Points
- **Frontend/Backend**: Frontend calls backend API for predictions and corrections.
- **Backend/Database**: Backend fetches training data via database API, not direct DB access.
- **Monitoring**: All APIs expose health endpoints for Prometheus scraping.
- **Orchestration**: Prefect flows trigger retraining and data analysis jobs.

## Key Files & Directories
- `docker-compose.yml`: Service orchestration and networking.
- `backend/main.py`: FastAPI prediction API.
- `database/main.py`: FastAPI database API (data/statistics).
- `database/modules/models.py`: SQLAlchemy models.
- `mlruns/`: MLflow model artifacts.
- `grafana_mnistretrain/provisioning/`: Grafana dashboards/datasources.
- `.github/workflows/`: CI/CD pipelines.

## Example: Fetching Training Data for ML Pipeline
```python
import requests
resp = requests.get('http://database-app:8011/dataframe?limit=1000')
df = pd.DataFrame(resp.json())
```

## Example: Posting Training Stats
```python
import requests
stats = {"model": "rf_v1", "accuracy": 0.91, "cpu_time": 12.3}
requests.post('http://database-app:8011/stats', json=stats)
```

---

For unclear conventions or missing documentation, ask for clarification or review the latest `README.md` and workflow files.
