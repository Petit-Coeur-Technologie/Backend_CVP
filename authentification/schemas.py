from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class UtilisateurCreate(BaseModel):
    quartier_id: Optional[int]
    nom_prenom: str
    email: str
    tel: str
    genre: bool
    copie_PI: str
    role: str
    mot_de_passe: str



class PmeCreate(BaseModel):
    id: int
    nom_pme: str
    description: str
    zone_intervention: str
    logo_pme: str
    utilisateur_id: int



class ClientCreate(BaseModel):
    id: int
    type_client: bool
    num_rccm: str
    nom_entreprise: str
    photo_profil: str
    utilisateur_id: int
     


class VilleCreate(BaseModel):
    id: int
    nom: str



class CommuneCreate(BaseModel):
    id: int
    nom: str
    ville_id: int


class QuartierCreate(BaseModel):
    id: int
    nom: str
    commune_id: int


class AbonnementCreate(BaseModel):
    id: int
    num_abonnement: str
    montant_abonnement: int
    debut_abonnement: date
    fin_abonnement: date
    status_abonnement: bool
    pme_id: int
    client_id: int



class CalendrierCreate(BaseModel):
    id: int
    jour_passage: date
    heure_passage: time
    creation: date
    mise_a_jour: date
    pme_id: int


class ConfPassageCreate(BaseModel):
    id: int
    date_confirmation: date
    confirmation: str
    calendrier_id: int

