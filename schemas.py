from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, time
from models import Ville

class utilisateur(BaseModel):
    quartier_id: int
    nom_prenom: str
    email: EmailStr
    mot_de_passe: str
    tel: str
    genre: str
    copie_PI: str
    role: str
    statut_actif: str
    date_inscription: date
    note: Optional[int]
    photo_profil: Optional[int]
    

class utilisateurCreate(BaseModel):
    nom_prenom: str
    email: str
    mot_de_passe: str
    tel: str
    genre: str
    copie_PI: str
    role: str
    note: Optional[int]
    photo: str
   
    class Config:
        orm_mode: True
        
class utilisateurRep(BaseModel):
    nom_prenom: str
    email: EmailStr
    tel: str
    genre: str
    photo: str
    role: str
    note: Optional[int]
    date_inscription: date
    
    class Config:
        orm_mode: True

class pme(utilisateur):
    id: int
    nom_pme: str
    description: str
    zone_intervention: str
    logo_pme: str
    tarif_abonnement: int

class pmeCreate(utilisateurCreate):
    nom_pme: str
    description: str
    zone_intervention: str
    logo_pme: str
    tarif_abonnement: int

    class Config:
        orm_mode: True
        
class pmeRep(utilisateurRep):
    nom_pme: str
    description: str
    zone_intervention: str
    logo_pme: str
    tarif_abonnement: int
    
    class Config:
        orm_mode: True
        
        
class client(utilisateur):
    id: int
    num_rccm: str
    nom_entreprise: str
    photo_profil: str

class clientCreateEntreprise(utilisateurCreate):
    num_rccm: str
    nom_entreprise: str
  
    class Config:
        orm_mode: True
        
        
class clientRepEntreprise(utilisateurRep):
    nom_entreprise: str
    
    class Config:
        orm_mode: True


class clientCreateMenage(utilisateurCreate):
    pass

    class Config:
        orm_mode: True

class clientRepMenage(utilisateurRep):
    pass

    class Config:
        orm_mode: True
        
class ville(BaseModel):
    id: int
    nom: str

class villeCreate(ville):
    nom: str
    
    class Config:
        orm_mode: True


class villeRep(ville):
    nom: str
    
    class Config:
        orm_mode: True
        
        
class Commune(BaseModel):
    id: int
    nom: str
    ville_id: int


class CommuneCreate(Commune):
    nom: str
    ville_id: int
    
    class Config:
        orm_mode: True
   
class CommuneRep(Commune):
    nom: str
    ville_id: int
    
    class Config:
        orm_mode: True


class Quartier(BaseModel):
    id: int
    nom: str
    commune_id: int

class QuartierCreate(Quartier):
    nom: str
    commune_id: int
    
    class Config:
        orm_mode: True

   
class QuartierRep(Quartier):
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


class AbonnementRep(BaseModel):
    num_abonnement: str
    montant_abonnement: int
    debut_abonnement: date
    fin_abonnement: date
    status_abonnement: bool
    

class CalendrierCreate(BaseModel):
    jour_passage: date
    heure_passage: time
    creation: date
    mise_a_jour: date
    
    class Config:
        orm_mode: True
        
class CalendrierRep(BaseModel):
    jour_passage: date
    heure_passage: time
    creation: date
    mise_a_jour: date
    
    class Config:
        orm_mode: True

class Calendrier(BaseModel):
    id: int
    jour_passage: date
    heure_passage: time
    creation: date
    mise_a_jour: date
    pme_id: int
    

class ConfPassageCreate(BaseModel):
    date_confirmation: date
    confirmation: str
    
    class Config:
        orm_mode: True

class ConfPassage(BaseModel):
    id: int
    date_confirmation: date
    confirmation: str
    calendrier_id: int

class ConfPassageRep(BaseModel):
    date_confirmation: date
    confirmation: str
    
    class Config:
        orm_mode: True  
        
        
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    