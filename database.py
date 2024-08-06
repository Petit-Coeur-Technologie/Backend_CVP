from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de connexion à la base de données
DATABASE_URL = 'postgresql://postgres:1234@localhost/pme_api'

# Création de l'engine
engine = create_engine(DATABASE_URL)

# Configuration de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de données de déclaration
Base = declarative_base()
