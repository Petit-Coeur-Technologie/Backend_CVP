from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from passlib.context import CryptContext
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Création de l'application FastAPI
app = FastAPI()

# Configuration de la base de données PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://votre_utilisateur:votre_mot_de_passe@votre_hote:votre_port/votre_base_de_données"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modèle de données pour un utilisateur
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)

# Création des tables dans la base de données
Base.metadata.create_all(bind=engine)

# Modèle Pydantic pour la validation des données d'entrée
class UserCreate(BaseModel):
    email: str
    password: str

# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Création d'un contexte pour le hashage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fonction pour générer un token unique
def generate_password_reset_token():
    return uuid.uuid4().hex

# Fonction pour envoyer un email de confirmation
def send_confirmation_email(email, token):
    # Création du message
    message = MIMEMultipart()
    message['From'] = 'votre_email@exemple.com'
    message['To'] = email
    message['Subject'] = 'Confirmez votre inscription'
    body = f"Cliquez sur ce lien pour confirmer votre inscription: http://votre_site.com/confirm?token={token}"
    message.attach(MIMEText(body, 'plain'))

    # Envoi de l'email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('votre_email@exemple.com', 'votre_mot_de_passe')
        smtp.sendmail('votre_email@exemple.com', email, message.as_string())

# Route pour créer un nouvel utilisateur
@app.post("/signup/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Vérification si l'email existe déjà
    db_user = db.query(User).filter(by=User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")

    # Hasher le mot de passe
    hashed_password = pwd_context.hash(user.password)

    # Créer un nouvel utilisateur
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Générer un token et envoyer l'email de confirmation
    token = generate_password_reset_token()
    send_confirmation_email(user.email, token)

    return {"message": "Utilisateur créé avec succès"}
