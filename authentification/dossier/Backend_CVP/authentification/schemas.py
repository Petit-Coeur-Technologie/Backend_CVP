from pydantic import BaseModel
from typing import Optional

class UtilisateurBase(BaseModel):
    nom_prenom: str
    email: str
    tel: str
    genre: bool

class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: str
    quartier_id: int

class Utilisateur(UtilisateurBase):
    id: int
    quartier_id: int  
    pmes: List['Pme'] = []
    clients: List['Client'] = []

    class Config:
        orm_mode = True

class PmeBase(BaseModel):
    nom_pme: str
    description: str
    zone_intervention: str
    logo: str
    pi_rep: str

class PmeCreate(PmeBase):
    utilisateur_id: int

class Pme(PmeBase):
    id: int

    class Config:
        orm_mode = True

class ClientCreateBase(BaseModel):
    email: str
    tel: str
    genre: bool
    pi_client: str


class MenageCreate(ClientCreateBase):
    nom_prenom: str
    type_client: str = Field(default="menage")


class EntrepriseCreate(ClientCreateBase):
    nom_prenom: str
    num_rccm: str
    nom_entreprise: str
    type_client: str = Field(default="entreprise")


class Client(BaseModel):
    id: int
    nom_prenom: str
    email: str
    tel: str
    genre: bool
    type_client: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    nom_prenom: Optional[str] = None
    email: Optional[str] = None
