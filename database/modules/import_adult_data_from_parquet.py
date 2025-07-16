import os
import pandas as pd
from sqlalchemy.orm import sessionmaker
from models import Workclass, Education, MaritalStatus, Occupation, NativeCountry, ClassLabel, Person
import mysql_initialize as mysql_initialize

def get_engine_local():
    mysql_initialize.DB_HOST = os.getenv("DB_HOST", "localhost")
    return mysql_initialize.get_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine_local())

def get_session():
    return SessionLocal()

def get_or_create(session, model, name):
    obj = session.query(model).filter_by(name=name).first()
    if not obj:
        obj = model(name=name)
        session.add(obj)
        session.commit()
    return obj

def import_parquet(filepath, session):
    df = pd.read_parquet(filepath)
    for _, row in df.iterrows():
        workclass_obj = get_or_create(session, Workclass, row['workclass'])
        education_obj = get_or_create(session, Education, row['education'])
        marital_status_obj = get_or_create(session, MaritalStatus, row['marital_status'])
        occupation_obj = get_or_create(session, Occupation, row['occupation'])
        native_country_obj = get_or_create(session, NativeCountry, row['native_country'])
        class_label_obj = get_or_create(session, ClassLabel, row['class_label'])
        person = Person(
            age=int(row['age']),
            workclass_id=workclass_obj.id,
            education_id=education_obj.id,
            marital_status_id=marital_status_obj.id,
            occupation_id=occupation_obj.id,
            capital_gain=int(row['capital_gain']),
            capital_loss=int(row['capital_loss']),
            hours_per_week=int(row['hours_per_week']),
            native_country_id=native_country_obj.id,
            class_label_id=class_label_obj.id
        )
        session.add(person)
    session.commit()

def main():
    session = get_session()
    print("Import de adult_all.parquet...")
    parquet_path = os.path.join(os.path.dirname(__file__), "../adult", "adult_all.parquet")
    import_parquet(parquet_path, session)
    session.close()
    print("Import terminé.")

if __name__ == "__main__":
    main()