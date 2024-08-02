from sqlalchemy import create_engine
from .models import Base  # Import du module models local
from sqlalchemy.orm import declarative_base, sessionmaker

# Remplacez par vos informations de connexion
SQLALCHEMY_DATABASE_URL = "postgresql://villepropre_db_user:Abdasalimbangs7@localhost/villepropre_db"

# Création du moteur de base de données avec echo activé pour le débogage
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Création des tables dans la base de données si elles n'existent pas
Base.metadata.create_all(bind=engine)

# Configuration de la base déclarative pour les modèles
Base = declarative_base()

# Création d'un constructeur de session pour gérer les transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Définir une fonction pour créer une nouvelle session à chaque requête
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



