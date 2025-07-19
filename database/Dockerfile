FROM python:3.11-slim

WORKDIR /app
# COPY . /app
COPY adult ./adult
COPY modules ./modules
COPY main.py ./
COPY api_base.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8011"]
