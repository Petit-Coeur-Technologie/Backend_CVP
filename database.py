from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

<<<<<<< HEAD


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:2413@localhost/Ville_propre'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    
    try :
        yield db
    finally :
        db.close()

=======
# URL de connexion à la base de données
DATABASE_URL = 'postgresql://postgres:1234@localhost/pme_api'

# Création de l'engine
engine = create_engine(DATABASE_URL)

# Configuration de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de données de déclaration
Base = declarative_base()
>>>>>>> 37298dd4e97f814e0c99fd6e150633548e0eea54
