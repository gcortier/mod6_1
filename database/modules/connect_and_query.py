from sqlalchemy.orm import sessionmaker
from database.modules.mysql_initialize import get_engine

# Crée une session SQLAlchemy connectée à la base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())

def get_session():
    """Retourne une session SQLAlchemy prête à l'emploi."""
    return SessionLocal()

if __name__ == "__main__":
    # Exemple d'utilisation : afficher les 5 premières personnes
    from modules.models import Person
    session = get_session()
    personnes = session.query(Person).limit(5).all()
    for p in personnes:
        print(f"id={p.id}, age={p.age}, class_id={p.class_id}")
    session.close()
