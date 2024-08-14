from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime



class Ville(BaseModel):
    id : int
    ville : str
    
    class Config:
        from_attributes = True

class Commune(BaseModel):
    id : int
    commune : str

    class Config:
        from_attributes = True
        
class Quartier(BaseModel):
    id: int
    quartier : str
    
    class Config:
        from_attributes = True


class SingleQuartier(Quartier):
    ville_id: int
    
    class Config:
        from_attributes = True
        
class Utilisateur(BaseModel):
    quartier_id : int
    nom_prenom : str
    tel : str
    genre : str
    email : EmailStr
    copie_pi : Optional[str] = None
    role: str
    create_at : datetime
    is_actif: bool
    update_at: datetime      
    
class UtilisateurBase(BaseModel):
    quartier_id : int
    nom_prenom : str
    tel : str
    genre : str
    email : EmailStr
    mot_de_passe: str
    copie_pi : Optional[str] = None
    role: str
    create_at : datetime
    is_actif: bool
    update_at: datetime
    

class UtilisateurCreate(UtilisateurBase):
    pass
    

class PmeCreate(UtilisateurCreate):
    nom_pme: str
    description: str
    zone_intervention: str
    num_enregistrement: str
    tarif_mensuel: int
    tarif_abonnement: int
    logo_pme: Optional[str] = None
    
class ClientCreate(BaseModel):
    num_rccm: Optional[str] = None
    nom_entreprise: Optional[str] = None
    
class UtilisateurOut(BaseModel):
    id: int
    quartier_id: int
    nom_prenom: str
    tel: str
    genre: str
    email: str
    copie_pi: str
    role: str
    create_at: datetime
    is_actif: bool
    update_at: datetime

    class Config:
        from_attributes = True
class UtilisateurLogin(BaseModel):
    email: EmailStr
    password : str
class PmeOut(BaseModel):
    id: int
    utilisateur: UtilisateurOut
    nom_pme: str
    description: str
    zone_intervention: str
    num_enregistrement: str
    tarif_mensuel: int
    tarif_abonnement: int
    logo_pme: str

    class Config:
        from_attributes = True
    
class ClientOut(BaseModel):
    id: int
    utilisateur: UtilisateurOut
    num_rccm: Optional[str] = None
    nom_entreprise: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    role : str