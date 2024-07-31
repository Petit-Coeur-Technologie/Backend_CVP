from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Utilisateurs(Base):
    __tablename__ = "Utilisateurs"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    quartier_id = Column(Integer, ForeignKey("quartier.id"))
    nom_prenom = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    mot_de_passe = Column(String, nullable=False)
    tel = Column(String, unique=True, index=True, nullable=False)
    genre = Column(Boolean, nullable=False, default=True)
    pmes = relationship('Pme', back_populates='utilisateur')
    clients = relationship('Client', back_populates='utilisateur')

class Pme(Base):
    __tablename__ = "Pme"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    utilisateur_id = Column(Integer, ForeignKey("Utilisateurs.id"))
    nom_pme = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False, index=True)
    zone_intervention = Column(String, nullable=False, index=True)
    logo = Column(String, nullable=False, index=True)
    pi_rep = Column(String, nullable=False, index=True)
    utilisateur = relationship('Utilisateurs', back_populates='pmes')

class Client(Base):
    __tablename__ = "Clients"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    utilisateur_id = Column(Integer, ForeignKey("Utilisateurs.id"))
    type_client = Column(Boolean, nullable=False, default=True)
    num_rccm = Column(String, nullable=False, index=True, unique=True)
    nom_entreprise = Column(String, nullable=False, index=True)
    pi_client = Column(String, nullable=False, index=True, unique=True)
    utilisateur = relationship('Utilisateurs', back_populates='clients')
