from pydantic import BaseModel
from typing import Optional

class UtilisateurBase(BaseModel):
    nom_prenom: str
    email: str
    tel: str
    genre: bool

class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: str

class Utilisateur(UtilisateurBase):
    id: int

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

class ClientBase(BaseModel):
    type_client: bool
    num_rccm: str
    nom_entreprise: str
    pi_client: str

class ClientCreate(ClientBase):
    utilisateur_id: int

class Client(ClientBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    nom_prenom: Optional[str] = None
    email: Optional[str] = None
