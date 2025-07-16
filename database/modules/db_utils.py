import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

def get_mysql_url():
    user = os.getenv('DB_USER', 'user')
    password = os.getenv('DB_PASSWORD', 'password')
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '3306')
    db = os.getenv('DB_NAME', 'adult')
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4"

def get_engine():
    url = get_mysql_url()
    return create_engine(url, echo=True, future=True)

def create_all_tables():
    engine = get_engine()
    Base.metadata.create_all(engine)

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
