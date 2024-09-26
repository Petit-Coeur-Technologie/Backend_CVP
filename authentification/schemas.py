from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, time

class UtilisateurCreate(BaseModel):
    quartier_id: Optional[int]
    nom_prenom: str
    email: EmailStr
    tel: str
    genre: bool
    copie_PI: str
    role: str
    mot_de_passe: str
    is_actif: bool
    date_creation: date

class Utilisateur(BaseModel):
    id: int
    quartier_id: Optional[int]
    nom_prenom: str
    email: str
    tel: str
    genre: bool
    copie_PI: str
    role: str

    class Config:
        orm_mode: True

class PmeCreate(BaseModel):
    nom_pme: str
    description: str
    zone_intervention: str
    logo_pme: str
    tarif_abonnement: int

class Pme(BaseModel):
    id: int
    nom_pme: str
    description: str
    zone_intervention: str
    logo_pme: str
    utilisateur_id: int

    class Config:
        orm_mode: True

class ClientCreate(BaseModel):
    type_client: bool
    num_rccm: str
    nom_entreprise: str
    photo_profil: str

class Client(BaseModel):
    id: int
    type_client: bool
    num_rccm: str
    nom_entreprise: str
    photo_profil: str
    utilisateur_id: int

    class Config:
        orm_mode: True



class VilleCreate(BaseModel):
    nom: str

class Ville(BaseModel):
    id: int
    nom: str

    class Config:
        orm_mode: True



class CommuneCreate(BaseModel):
    nom: str
    ville_id: int

class Commune(BaseModel):
    id: int
    nom: str
    ville_id: int

    class Config:
        orm_mode: True



class QuartierCreate(BaseModel):
    nom: str
    commune_id: int

class Quartier(BaseModel):
    id: int
    nom: str
    commune_id: int

    class Config:
        orm_mode: True



class AbonnementCreate(BaseModel):
    num_abonnement: str
    montant_abonnement: int
    debut_abonnement: date
    fin_abonnement: date
    status_abonnement: bool

class Abonnement(BaseModel):
    id: int
    num_abonnement: str
    montant_abonnement: int
    debut_abonnement: date
    fin_abonnement: date
    status_abonnement: bool
    pme_id: int
    client_id: int

    class Config:
        orm_mode: True



class CalendrierCreate(BaseModel):
    jour_passage: date
    heure_passage: time
    creation: date
    mise_a_jour: date

class Calendrier(BaseModel):
    id: int
    jour_passage: date
    heure_passage: time
    creation: date
    mise_a_jour: date
    pme_id: int

    class Config:
        orm_mode: True



class ConfPassageCreate(BaseModel):
    date_confirmation: date
    confirmation: str

class ConfPassage(BaseModel):
    id: int
    date_confirmation: date
    confirmation: str
    calendrier_id: int

    class Config:
        orm_mode: True
