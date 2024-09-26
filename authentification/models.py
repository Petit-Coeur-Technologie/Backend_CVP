from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Utilisateur(Base):
    __tablename__ = "Utilisateur"
    id = Column(Integer, primary_key=True, nullable=False)
    quartier_id = Column(Integer, ForeignKey("Quartier.id"))
    nom_prenom = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    mot_de_passe = Column(String, nullable=False)
    tel = Column(String, unique=True, index=True, nullable=False)
    genre = Column(Boolean, nullable=False, default=True)
    copie_PI = Column(String, nullable=False)
    role = Column(String, nullable=False)
    is_actif = Column(Boolean, server_default=False, nullable=False)
    date_creation = Column(TIMESTAMP(timezone=True), nullable=False, server_default=Text('now()'))

class Pme(Base):
    __tablename__ = "Pme"
    id = Column(Integer, ForeignKey("Utilisateur.id"), primary_key=True, nullable=False)
    nom_pme = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    zone_intervention = Column(String, nullable=False)
    logo_pme = Column(String, nullable=False)
    utilisateur = relationship('Utilisateur', back_ref='pme')
    tarif_abonnement = Column(Integer, nullable=False)

class Client(Base):
    __tablename__ = "Client"
    id = Column(Integer, ForeignKey("Utilisateur.id"), primary_key=True, nullable=False)
    type_client = Column(Boolean, nullable=False, default=True)
    num_rccm = Column(String, nullable=False, unique=True)
    nom_entreprise = Column(String, nullable=False, index=True)
    photo_profil = Column(String, nullable=False, unique=True)
    utilisateur = relationship('Utilisateur', back_ref='clients')

class Ville(Base):
    __tablename__ = "Ville"
    id = Column(Integer, primary_key=True, nullable=False)
    nom = Column(String, index=True, nullable=False)

class Commune(Base):
    __tablename__ = "Commune"
    id = Column(Integer, primary_key=True, nullable=False)
    ville_id = Column(Integer, ForeignKey("Ville.id"))
    nom = Column(String, index=True, nullable=False)

class Quartier(Base):
    __tablename__ = "Quartier"
    id = Column(Integer, primary_key=True, nullable=False)
    commune_id = Column(Integer, ForeignKey("Commune.id"))
    nom = Column(String, index=True, nullable=False)

class Abonnement(Base):
    __tablename__ = "Abonnement"
    id = Column(Integer, primary_key=True, nullable=False)
    pme_id = Column(Integer, ForeignKey("Pme.id"))
    client_id = Column(Integer, ForeignKey("Client.id"))
    num_abonnement = Column(String, nullable=False, unique=True)
    montant_abonnement = Column(Integer, nullable=False)
    debut_abonnement = Column(Date, nullable=False)
    fin_abonnement = Column(Date, nullable=False)
    status_abonnement = Column(Boolean, default=False, nullable=False)

class Calendrier(Base):
    __tablename__ = "Calendrier"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    pme_id = Column(Integer, ForeignKey("Pme.id"))
    jour_passage = Column(Date, nullable=False)
    heure_passage = Column(Time, nullable=False)
    creation = Column(Date, nullable=False)
    mise_a_jour = Column(Date, nullable=False)

class Conf_Passage(Base):
    __tablename__ = "Conf_passage"
    id = Column(Integer, primary_key=True, nullable=False)
    calendrier_id = Column(Integer, ForeignKey("Calendrier.id"))
    date_confirmation = Column(Date, nullable=False, index=True)
    confirmation = Column(String, nullable=False, index=True)
    
    
class OTP(Base):
    __tablename__ = 'otps'
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    otp = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
