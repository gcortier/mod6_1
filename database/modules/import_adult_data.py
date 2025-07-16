import os
from sqlalchemy.orm import Session, sessionmaker
from modules.models import Workclass, Education, MaritalStatus, Occupation, Relationship, NativeCountry, ClassLabel, Person
from database.modules.connect_and_query import get_session
import database.modules.mysql_initialize as mysql_initialize

# Correction pour usage local : forcer l'hôte MySQL à localhost si variable d'environnement non définie
def get_engine_local():
    # On force l'hôte à localhost si on est en local (hors Docker)
    mysql_initialize.DB_HOST = os.getenv("DB_HOST", "localhost")
    return mysql_initialize.get_engine()

# Remplace get_session pour utiliser l'engine local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine_local())

def get_session():
    return SessionLocal()

# data_file = os.path.join(os.path.dirname(__file__), "adult", "adult.data")

def get_or_create(session, model, name):
    obj = session.query(model).filter_by(name=name).first()
    if not obj:
        obj = model(name=name)
        session.add(obj)
        session.commit()
    return obj

def parse_line(line):
    # Les champs sont séparés par des virgules et parfois des espaces
    fields = [f.strip() for f in line.strip().split(",")]
    if len(fields) != 15:
        return None  # ligne vide ou mal formée
    return fields

def import_file(filepath, session):
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("|"):
                continue
            fields = parse_line(line)
            if not fields:
                continue
            age, workclass, fnlwgt, education, education_num, marital_status, occupation, relationship, _, _, capital_gain, capital_loss, hours_per_week, native_country, class_label = fields
            # On ignore race et sex (champs 9 et 10)
            workclass_obj = get_or_create(session, Workclass, workclass)
            education_obj = get_or_create(session, Education, education)
            marital_status_obj = get_or_create(session, MaritalStatus, marital_status)
            occupation_obj = get_or_create(session, Occupation, occupation)
            relationship_obj = get_or_create(session, Relationship, relationship)
            native_country_obj = get_or_create(session, NativeCountry, native_country)
            class_label_obj = get_or_create(session, ClassLabel, class_label)
            person = Person(
                age=int(age),
                workclass_id=workclass_obj.id,
                fnlwgt=int(fnlwgt),
                education_id=education_obj.id,
                education_num=int(education_num),
                marital_status_id=marital_status_obj.id,
                occupation_id=occupation_obj.id,
                relationship_id=relationship_obj.id,
                capital_gain=int(capital_gain),
                capital_loss=int(capital_loss),
                hours_per_week=int(hours_per_week),
                native_country_id=native_country_obj.id,
                class_id=class_label_obj.id
            )
            session.add(person)
    session.commit()

def main():
    session = get_session()
    print("Import de adult.data...")
    import_file(os.path.join(os.path.dirname(__file__), "adult", "adult.data"), session)
    print("Import de adult.test...")
    import_file(os.path.join(os.path.dirname(__file__), "adult", "adult.test"), session)
    session.close()
    print("Import terminé.")

if __name__ == "__main__":
    main()
