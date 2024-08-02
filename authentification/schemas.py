from pydantic import BaseModel, EmailStr

class Utilisateur(BaseModel):
    utilisateur_id: int
    id_quartier: int
    nom_prenom: str
    email: EmailStr # Utilise EmailStr pour valider automatiquement les formats d'email.
    mot_passe: str
    genre: str | None = None  # Genre peut être optionnel
    tel: str

    class Config:
        orm_mode = True

class PME(BaseModel):
    id_pme: int 
    id_user: int
    nom_pme: str
    description_pme: str
    zone_intervention: str
    num_enregistrement: str
    logo_pme: str  # Nous pouvons utiliser un champ de type UploadFile pour gérer les uploads
    piece_id_representant: str

    class Config:
        orm_mode = True
       
