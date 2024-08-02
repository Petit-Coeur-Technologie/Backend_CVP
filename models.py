from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from Sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, URLType

from .database import Base


##===============================================================##
##                       ADRESSE                                 ##
##===============================================================##

############################
#        Table Ville       #
############################
class Ville(Base):
    __tablename__ = "villes"
    
    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    ville = Column(
        String,
        nullable=False
    )
    
    commune = relationship(
        "Commune",
        backref="ville"
    )

############################
#        Table Commune     #
############################
class Commune(Base):
    __tablename__ = "communes"
    
    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    ville_id = Column(
        Integer,
        ForeignKey("villes.id")
    )
    commune = Column(
        String,
        nullable=False
    )
    
    quartier = relationship(
        "Quartier",
        backref="commune"
    )


############################
#        Table Quartier    #
############################
class Quartier(Base):
    __tablename__ = "quartiers"
    
    id = Column(
        Integer,
        primary_key=True
    )
    commune_id = Column(
        Integer,
        ForeignKey("communes.id")
    )
    quartier = Column(
        String,
        nullable=False   
    )
    
    utilisateur = Column(
        "Utilisateur",
        backref="quartier"
    )


##===============================================================##
##                    UTILISATEURS                               ##
##===============================================================##


##############################
#      Table Utilisateur     #
##############################

class Utilisateurs(Base):
    __tablename__ = "utilisateurs"
    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    quartier_id = Column(
        Integer,
        ForeignKey("quartiers.id")    
    )
    nom_prenom = Column(
        String,
        index=True,
        nullable=False
    )
    tel = Column(
        String,
        unique=True
    )
    genre = Column(
        String,
        nullable=False
    )
    email = Column(
        String,
        unique=True,
        nullable=False
    )
    mot_de_passe = Column(
        String,
        nullable=False
    )
    copie_pi = Column(
        String,
        nullable=False
    )
    role = Column(
        String,
        nullalbe=False
    )
    create_at = Column(
        DateTime,
        nullable=False
    )
    update_at = Column(
        DateTime,
        nullable=False
    )
    
    pme = relationship(
        "Pme",
        backref="utilisateur"
    )
    
    client = relationship(
        "Client",
        backref="utilisateur"
    )
    abonnement = relationship(
        "Abonnement",
        backref="utilisateur"
    )
    confcalronde = relationship(
        "ConfCalROnde",
        backref="utilisateur"
    )
    
##############################
#        Table PME           #
##############################
class Pme(Base):
    __tablename__ = "pmes"
    
    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    utilisateur_id = Column(
        Integer,
        ForeignKey("utilisateurs.id")
    )
    nom_pme = Column(
        String,
        nullable=False,
        index=True
    )
    description = Column(
        Text,
        nullable=False
    )
    zone_intervention = Column(
        String,
        nullable=False
    )
    num_enregistrement = Column(
        String,
        nullable=False
    )
    tarif_mensuel = Column(
        Integer,
        nullable=False
    )
    tarif_abonnement = Column(
        Integer,
        nullable=False
    )
    logo_pme = Column(
        String,
        nullable=False
    )
    
    
    abonnement = relationship(
        "Abonnement",
        backref="pme"
    )
    calronde = relationship(
        "CalRonde",
        backref="pme"
    )

##############################
#        Table Client        #
##############################
class Client(Base):
    __tablename__ = "Client"
    
    id = Column(
        Integer,
        primary_key=True
    )
    utilisateur_id = Column(
        Integer,
        ForeignKey("utilisateurs.id")
    )
    type_client = Column(
        String,
        nullable=False
    )
    num_rccm = Column(
        String,
        nullable=False
    )
    nom_entreprise = Column(
        String,
        nullable=False,
        index=True
    )
    pi_client = Column(
        String,
        nullable=False
    )



##===============================================================##
##                    Abonnements                                ##
##===============================================================##

##############################
#      Table Abonnement      #
##############################
class Abonnement(Base):
    __tablename__ = "abonnement"
    
    utilisateurs_id = Column(
        Integer,
        ForeignKey("utilisateurs.id")
    )
    pme_id = Column(
        Integer,
        ForeignKey("pmes.id")
    )
    num_abonnement = Column(
        String,
        nullable=False
    )
    tarif_abonnement = Column(
        Integer,
        nullable=False
    )
    status_abonnement = Column(
        Boolean,
        nullable=False
    )
    debut_abonnement = Column(
        DateTime,
        nullable=False
    )
    fin_abonnement = Column(
        DateTime,
        nullable=False
    )



##===============================================================##
##         Calendrier et confirmation des rondes                 ##
##===============================================================##

##############################
#      Table CalRonde       #
##############################

class CalROnde(Base):
    __tablename__ = "calrondes"
    
    id = Column(
        Integer,
        primary_key=True
    )
    pme_id = Column(
        Integer,
        ForeignKey("pmes.id")
    )
    jour_passage = Column(
        String,
        nullable=False
    )
    heure_passage = Column(
        String,
        nullable=False
    )
    date_creation = Column(
        DateTime,
        nullable=False
    )
    date_maj = Column(
        DateTime
    )
    
    confcalronde = relationship(
        "ConfCalROnde",
        backref="calrondes"
    )


##############################
#    Table ConfCalRonde      #
##############################  

class ConfCalRonde(Base):
    __tablename__ = "confcalronde"
    
    id = Column(
        Integer,
        primary_key=True
    )
    calronde_id = Column(
        Integer,
        ForeignKey("calrondes.id")
    )
    utilisateur_id = Column(
        Integer,
        ForeignKey("utilisateurs.id")
    )
    conf_passage = Column(
        Boolean,
        nullable=False
    )
    date_conf_passage = Column(
        DateTime,
        nullable=False
    )