from sqlalchemy import Column, Integer, String, Date, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine

class Utilisateur(Base):
    __tablename__ = 'utilisateurs'
    id = Column(Integer, primary_key=True, index=True)
    quartier_id = Column(Integer, index=True)
    nom_prenom = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    mot_de_passe = Column(String)
    tel = Column(String)
    genre = Column(String)
    copie_PI = Column(String)
    role = Column(String)
    statut_actif = Column(String)
    date_inscription = Column(Date)
    note = Column(Integer, nullable=True)
    photo_profil = Column(String, nullable=True)

class Pme(Base):
    __tablename__ = 'pmes'
    id = Column(Integer, primary_key=True, index=True)
    nom_pme = Column(String)
    description = Column(String)
    zone_intervention = Column(String)
    logo_pme = Column(String)
    tarif_abonnement = Column(Integer)
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'))

    utilisateur = relationship("Utilisateur")

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    num_rccm = Column(String, nullable=True)
    nom_entreprise = Column(String, nullable=True)
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'))

    utilisateur = relationship("Utilisateur")

class Abonnement(Base):
    __tablename__ = 'abonnements'
    id = Column(Integer, primary_key=True, index=True)
    num_abonnement = Column(String)
    montant_abonnement = Column(Integer)
    debut_abonnement = Column(Date)
    fin_abonnement = Column(Date)
    status_abonnement = Column(Boolean)
    pme_id = Column(Integer, ForeignKey('pmes.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))

class Calendrier(Base):
    __tablename__ = 'calendriers'
    id = Column(Integer, primary_key=True, index=True)
    jour_passage = Column(Date)
    heure_passage = Column(Time)
    creation = Column(Date)
    mise_a_jour = Column(Date)
    pme_id = Column(Integer, ForeignKey('pmes.id'))

class ConfPassage(Base):
    __tablename__ = 'conf_passages'
    id = Column(Integer, primary_key=True, index=True)
    date_confirmation = Column(Date)
    confirmation = Column(String)
    calendrier_id = Column(Integer, ForeignKey('calendriers.id'))


class Ville(Base):
    __tablename__ = 'villes'
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
# Crée toutes les tables dans la base de données
Base.metadata.create_all(bind=engine)
