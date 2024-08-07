import os
import uuid
from datetime import datetime
from typing import Union, Optional
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.middleware.cors import CORSMiddleware
import time
from sqlalchemy.orm import Session
from typing import List
from models import *
from database import engine, SessionLocal, get_db, Base
import schemas
from utils import hash_password


Base.metadata.create_all(bind=engine)

app = FastAPI()

# dossiers de destination pour les uploads
UPLOAD_DIRECTORY_COPIE_PI = "Uploads/copie_pi"
UPLOAD_DIRECTORY_LOGO_PME = "Uploads/logo_pme"

# Verifier l'existence des dossiers
os.makedirs(UPLOAD_DIRECTORY_COPIE_PI, exist_ok=True)
os.makedirs(UPLOAD_DIRECTORY_LOGO_PME, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get('/')
def index_root():
    return {"message": "Bienvenue sur l'interface de developpement de conakry ville propre"}


@app.get('/villes', response_model=List[schemas.Ville], tags=["Villes"])
def get_villes(db: Session = Depends(get_db)):
    
    villes = db.query(Ville).all()
    
    return villes

@app.get('/villes/{id}/communes', response_model=List[schemas.Commune], tags=["Villes"])
def get_com_by_villes(id: int, db: Session = Depends(get_db)):
    
    communes = db.query(Commune).filter(Commune.ville_id==id).all()
    
    return communes

@app.get('/communes', response_model=List[schemas.Commune], tags=["Communes"])
def get_communes(db: Session = Depends(get_db)):
    
    communes = db.query(Commune).all()
    
    return communes

@app.get('/communes/{id}/quartiers', response_model=List[schemas.Quartier], tags=["Communes"])
def get_quartiers_by_com(id:int, db: Session = Depends(get_db)):
    
    quartiers = db.query(Quartier).filter(Quartier.commune_id==id).all()
    
    return quartiers

@app.get('/quartiers', response_model=List[schemas.Quartier], tags=["Quartier"])
def get_quartiers(db: Session = Depends(get_db)):
    
    quartiers = db.query(Quartier).all()
    
    return quartiers



@app.post("/pme", response_model=schemas.PmeOut, tags=["Pme"])
async def register_pme(
    quartier_id: int = Form(...),
    nom_prenom: str = Form(...),
    tel: str = Form(...),
    genre: str = Form(...),
    email: str = Form(...),
    mot_de_passe: str = Form(...),
    copie_pi: UploadFile = File(...),
    create_at: datetime = Form(...),
    update_at: datetime = Form(...),
    is_actif: bool = Form(...),
    nom_pme: str = Form(...),
    description: str = Form(...),
    zone_intervention: str = Form(...),
    num_enregistrement: str = Form(...),
    tarif_mensuel: int = Form(...),
    tarif_abonnement: int = Form(...),
    logo_pme: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    
    
    # Vérifier si l'email ou le numéro de téléphone existe déjà
    existing_user = db.query(Utilisateur).filter(
        (Utilisateur.email == email) | (Utilisateur.tel == tel)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'email ou le numéro de téléphone existe déjà dans la base de données."
    )
     
    #hasher le mot de passe
    hashed_password = hash_password(mot_de_passe)
    
    # Sauvegarde du fichier copie_pi
    copie_pi_file_name = f"{uuid.uuid4()}_{copie_pi.filename}"
    copie_pi_file_path = os.path.join(UPLOAD_DIRECTORY_COPIE_PI, copie_pi_file_name)
    
    with open(copie_pi_file_path, "wb") as buffer:
        buffer.write(await copie_pi.read())
    
    # Sauvegarde du fichier logo_pme
    logo_pme_file_name = f"{uuid.uuid4()}_{logo_pme.filename}"
    logo_pme_file_path = os.path.join(UPLOAD_DIRECTORY_LOGO_PME, logo_pme_file_name)
    
    with open(logo_pme_file_path, "wb") as buffer:
        buffer.write(await logo_pme.read())
    
    # Création de l'utilisateur
    db_utilisateur = Utilisateur(
        quartier_id=quartier_id,
        nom_prenom=nom_prenom,
        tel=tel,
        genre=genre,
        email=email,
        mot_de_passe=hashed_password,
        copie_pi=copie_pi_file_name,
        role="pme",
        create_at=create_at,
        is_actif=is_actif,
        update_at=update_at,
    )
    db.add(db_utilisateur)
    db.commit()
    db.refresh(db_utilisateur)
    
    # Création de l'entité PME
    db_pme = Pme(
        utilisateur_id=db_utilisateur.id,
        nom_pme=nom_pme,
        description=description,
        zone_intervention=zone_intervention,
        num_enregistrement=num_enregistrement,
        tarif_mensuel=tarif_mensuel,
        tarif_abonnement=tarif_abonnement,
        logo_pme=logo_pme_file_name,
    )
    db.add(db_pme)
    db.commit()
    db.refresh(db_pme)

    return db_utilisateur

@app.get('/pmes', response_model=List[schemas.PmeOut], tags=['Pme'])
def get_pmes(db : Session = Depends(get_db)):
    
    pmes = db.query(Pme).outerjoin(Utilisateur).all()

    # Transformez les résultats en format approprié
    pme_list = []
    for pme in pmes:
        pme_data = schemas.PmeOut(
            id=pme.id,
            utilisateur=schemas.UtilisateurOut(
                id=pme.utilisateur.id,
                quartier_id=pme.utilisateur.quartier_id,
                nom_prenom=pme.utilisateur.nom_prenom,
                tel=pme.utilisateur.tel,
                genre=pme.utilisateur.genre,
                email=pme.utilisateur.email,
                mot_de_passe=pme.utilisateur.mot_de_passe,
                copie_pi=pme.utilisateur.copie_pi,
                role=pme.utilisateur.role,
                create_at=pme.utilisateur.create_at,
                is_actif=pme.utilisateur.is_actif,
                update_at=pme.utilisateur.update_at,
            ),
            nom_pme=pme.nom_pme,
            description=pme.description,
            zone_intervention=pme.zone_intervention,
            num_enregistrement=pme.num_enregistrement,
            tarif_mensuel=pme.tarif_mensuel,
            tarif_abonnement=pme.tarif_abonnement,
            logo_pme=pme.logo_pme
        )
        pme_list.append(pme_data)

    return pme_list
     

@app.post("/client", tags=["Clients"])
async def create_client(
    role: str = Form(...),
    quartier_id: int = Form(...),
    nom_prenom: str = Form(...),
    tel: str = Form(...),
    genre: str = Form(...),
    email: str = Form(...),
    mot_de_passe: str = Form(...),
    copie_pi: UploadFile = File(...),
    create_at: datetime = Form(...),  # Recevoir comme chaîne
    is_actif: bool = Form(...),
    update_at: datetime = Form(...),  # Recevoir comme chaîne
    num_rccm: Optional[str] = Form(None),
    nom_entreprise: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    
    #hasher le mot de passe
    hashed_password2 = hash_password(mot_de_passe)
    
    # Sauvegarde du fichier copie_pi
    copie_pi_file_name = f"{uuid.uuid4()}_{copie_pi.filename}"
    copie_pi_file_path = os.path.join(UPLOAD_DIRECTORY_COPIE_PI, copie_pi_file_name)
    
    with open(copie_pi_file_path, "wb") as buffer:
        buffer.write(await copie_pi.read())
        
    # Création de l'utilisateur
    db_utilisateur = Utilisateur(
        quartier_id=quartier_id,
        nom_prenom=nom_prenom,
        tel=tel,
        genre=genre,
        email=email,
        mot_de_passe=hashed_password2,
        copie_pi=copie_pi.filename,
        role=role,
        create_at=create_at,
        is_actif=is_actif,
        update_at=update_at,
    )
    db.add(db_utilisateur)
    db.commit()
    db.refresh(db_utilisateur)
    
    if role == "entreprise" and num_rccm and nom_entreprise:
        # Création de l'entité Client pour entreprise
        db_client = Client(
            utilisateur_id=db_utilisateur.id,
            num_rccm=num_rccm,
            nom_entreprise=nom_entreprise
        )
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
    
    return db_utilisateur