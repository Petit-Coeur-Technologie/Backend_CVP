from sqlalchemy import create_engine
from .models import Base  # Import du module models local
from sqlalchemy.orm import declarative_base, sessionmaker
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Remplacez par vos informations de connexion
SQLALCHEMY_DATABASE_URL = "postgresql://villepropre_db_user:Abdasalimbangs7@localhost/villepropre_db"

# Création du moteur de base de données avec echo activé pour le débogage
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Création des tables dans la base de données si elles n'existent pas
Base.metadata.create_all(bind=engine)

# Configuration de la base déclarative pour les modèles
Base = declarative_base()

# Création d'un constructeur de session pour gérer les transactions
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Définir une fonction pour créer une nouvelle session à chaque requête
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



load_dotenv()  # Charger les variables d'environnement depuis .env

class ClientSMTP:
    def __init__(self, hote, port, utilisateur, mot_de_passe):
        self.hote = hote
        self.port = port
        self.utilisateur = utilisateur
        self.mot_de_passe = mot_de_passe
        self.contexte = ssl.create_default_context()

    def __enter__(self):
        self.serveur = smtplib.SMTP(self.hote, self.port)
        self.serveur.starttls(context=self.contexte)
        self.serveur.login(self.utilisateur, self.mot_de_passe)
        return self.serveur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.serveur.quit()

# Récupérer les informations depuis le fichier .env
HOTE_SMTP = os.getenv('SMTP_HOST')
PORT_SMTP = int(os.getenv('SMTP_PORT'))
UTILISATEUR_SMTP = os.getenv('SMTP_USER')
MOT_DE_PASSE_SMTP = os.getenv('SMTP_PASSWORD')

# Fonction pour envoyer un email
def envoyer_email(destinataire, sujet, corps):
    with ClientSMTP(HOTE_SMTP, PORT_SMTP, UTILISATEUR_SMTP, MOT_DE_PASSE_SMTP) as smtp:
        message = MIMEMultipart()
        message["From"] = UTILISATEUR_SMTP
        message["To"] = destinataire
        message["Subject"] = sujet
        message.attach(MIMEText(corps, "plain"))
        smtp.sendmail(UTILISATEUR_SMTP, destinataire, message.as_string())


