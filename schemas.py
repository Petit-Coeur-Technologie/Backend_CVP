from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime



class Ville(BaseModel):
    id : int
    ville : str
    
    class Config:
        orm_mode = True

class Commune(BaseModel):
    id : int
    commune : str

    class Config:
        orm_mode = True
        
class Quartier(BaseModel):
    id: int
    quartier : str
    


class SingleQuartier(Quartier):
    ville_id: int
    
    class Config:
        orm_mode = True
        
        
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
    
class ClientCreate(UtilisateurCreate):
    num_rccm: Optional[str] = None
    nom_entreprise: Optional[str] = None
    
class PmeOut(PmeCreate):
    id: int
    
class Clientout(ClientCreate):
    id : int