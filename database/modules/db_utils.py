import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flights.data.models import Base, Carrier, Airport, TimeBlock, Flight

def get_mysql_url():
    user = os.getenv('DB_USER', 'user')
    password = os.getenv('DB_PASSWORD', 'password')
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '3306')
    db = os.getenv('DB_NAME', 'flights')
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

def fetch_full_dataframe():
    from .db_utils import get_session
    session = get_session()
    # Jointure pour récupérer toutes les infos nécessaires
    query = session.query(
        Person.id,
        Person.age,
        Workclass.name.label('workclass'),
        Education.name.label('education'),
        MaritalStatus.name.label('marital_status'),
        Occupation.name.label('occupation'),
        Person.capital_gain,
        Person.capital_loss,
        Person.hours_per_week,
        NativeCountry.name.label('native_country'),
        ClassLabel.name.label('class_label')
    ).join(Workclass, Person.workclass_id == Workclass.id)
    query = query.join(Education, Person.education_id == Education.id)
    query = query.join(MaritalStatus, Person.marital_status_id == MaritalStatus.id)
    query = query.join(Occupation, Person.occupation_id == Occupation.id)
    query = query.join(NativeCountry, Person.native_country_id == NativeCountry.id)
    query = query.join(ClassLabel, Person.class_label_id == ClassLabel.id)
    df = pd.DataFrame(query.all(), columns=[c['name'] for c in query.column_descriptions])
    session.close()
    return df
