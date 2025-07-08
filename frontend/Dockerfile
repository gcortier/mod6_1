FROM python:3.11-slim
WORKDIR /app
COPY app.py .
COPY requirements.txt ./
RUN pip install -r requirements.txt
EXPOSE 8501
# commande locale : streamlit run app.py
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
