<<<<<<< HEAD
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Union
from datetime import datetime, date



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
        
class QuartierOut(BaseModel):
    id: int
    quartier : str
    
    class Config:
        from_attributes = True


class SingleQuartier(QuartierOut):
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

=======
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
        
        
>>>>>>> 37298dd4e97f814e0c99fd6e150633548e0eea54
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
<<<<<<< HEAD
    user_id: str | None = None
    role : str
    

class AbonnementBase(BaseModel):
    pme_id: int
    num_abonnement: str
    tarif_abonnement: int
    status_abonnement: str 
    debut_abonnement: datetime
    fin_abonnement: Optional[date]
   

class AbonnementCreate(AbonnementBase):
    pass

class AbonnementOut(AbonnementBase):
    id: int
    status_abonnement: str
    utilisateurs_id: int

    class Config:
        from_attributes = True
        from_attributes = True

class AbonneeOut(BaseModel):
    utilisateur : Union[UtilisateurOut, ClientOut]
    status_abonnement: str
    debut_abonnement: datetime

class ma_pme_out(BaseModel):
    pme: PmeOut


class UpdatePme(BaseModel):
    nom_pme: str
    description: str
    zone_intervention: str
    tarif_mensuel: int
    tarif_abonnement: int
    logo_pme: str   

class UpdatePassword(BaseModel):
    old_password: str
    new_password: str

# les schema pour la mise à jour du Client
class ClientUpdateBase(BaseModel):
    quartier_id: Optional[int] = None
    nom_prenom: Optional[str] = None
    tel: Optional[str] = None
    genre: Optional[str] = None
    email: Optional[EmailStr] = None
    copie_pi: Optional[str] = None
    is_actif: Optional[bool] = None
    num_rccm: Optional[str] = None
    nom_entreprise: Optional[str] = None

class EntrepriseClientUpdate(ClientUpdateBase):
    num_rccm: Optional[str] = None
    nom_entreprise: Optional[str] = None

class MenageClientUpdate(ClientUpdateBase):
    pass

class CommentIn(BaseModel):
    utilisateur_id: int
    pme_id: int
    message: str
    note: Optional[int]
    date_publicat: datetime

class CommentOut(BaseModel):
    message: str
    note: Optional[int]
    date_publicat: datetime

class Commentshow(BaseModel):
    message: str
    auteur: int
    note: Optional[int]
    date_publicat: datetime

=======
    username: Optional[str] = None
    
>>>>>>> 37298dd4e97f814e0c99fd6e150633548e0eea54
