from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "adult")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_engine():
    return create_engine(SQLALCHEMY_DATABASE_URL)

def init_db():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("MySQL DB initialized with SQLAlchemy models.")
