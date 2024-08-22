import os
import uuid
from datetime import datetime
from typing import  Optional, Union
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from models import *
from jwt import InvalidTokenError
from database import engine, get_db, Base
import schemas
from utils import hash_password, verify_password, create_access_token, role_required
from schemas import ClientOut


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static/Uploads"), name="uploads")
# dossiers de destination pour les uploads
UPLOAD_DIRECTORY_COPIE_PI = "static/uploads/copie_pi"
UPLOAD_DIRECTORY_LOGO_PME = "static/uploads/logo_pme"

# Verifier l'existence des dossiers
os.makedirs(UPLOAD_DIRECTORY_COPIE_PI, exist_ok=True)
os.makedirs(UPLOAD_DIRECTORY_LOGO_PME, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_clients_by_pme(db: Session, pme_id: int):
    return db.query(Client).join(Abonnement).filter(Abonnement.pme_id == pme_id).all()

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
def get_quartier(db: Session = Depends(get_db)):
    
    quartiers = db.query(Quartier).all()
    
    return quartiers

@app.get('/quartiers/{quartier_id}', response_model=schemas.Quartier, tags=["Quartier"])
def get_quartier(quartier_id: int, db: Session = Depends(get_db)):
    
    quartier = db.query(Quartier).filter(Quartier.id == quartier_id).first()
    
    if quartier is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Il n'y a pas de quartier qui correspond à l'id fourni")
    
    return quartier



@app.post("/pme", status_code=status.HTTP_201_CREATED, response_model=schemas.PmeOut, tags=["Pme"])
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
    existing_pme = db.query(Pme).filter(
        (Pme.nom_pme == nom_pme) | (Pme.num_enregistrement == num_enregistrement)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'email ou le numéro de téléphone existe déjà dans la base de données."
        )
    if existing_pme:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La pme ou le numéro d'enregistrement existe déjà dans le système"
        )
    # Hasher le mot de passe
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


    copie_pi_url = f"/static/uploads/copie_pi/{copie_pi_file_name}"
    logo_pme_url = f"/static/uploads/logo_pme/{logo_pme_file_name}"

    # Création de l'utilisateur
    db_utilisateur = Utilisateur(
        quartier_id=quartier_id,
        nom_prenom=nom_prenom,
        tel=tel,
        genre=genre,
        email=email,
        mot_de_passe=hashed_password,
        copie_pi=copie_pi_url,
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
        logo_pme=logo_pme_url,
    )
    db.add(db_pme)
    db.commit()
    db.refresh(db_pme)

    # Convertir en dictionnaire pour la réponse
    pme_data = {
        "id": db_pme.id,
        "utilisateur": {
            "id": db_utilisateur.id,
            "quartier_id": db_utilisateur.quartier_id,
            "nom_prenom": db_utilisateur.nom_prenom,
            "tel": db_utilisateur.tel,
            "genre": db_utilisateur.genre,
            "email": db_utilisateur.email,
            "copie_pi": db_utilisateur.copie_pi,
            "role": db_utilisateur.role,
            "create_at": db_utilisateur.create_at.isoformat(),
            "is_actif": db_utilisateur.is_actif,
            "update_at": db_utilisateur.update_at.isoformat(),
        },
        "nom_pme": db_pme.nom_pme,
        "description": db_pme.description,
        "zone_intervention": db_pme.zone_intervention,
        "num_enregistrement": db_pme.num_enregistrement,
        "tarif_mensuel": db_pme.tarif_mensuel,
        "tarif_abonnement": db_pme.tarif_abonnement,
        "logo_pme": db_pme.logo_pme,
    }

    # Utiliser `parse_obj` pour créer l'instance Pydantic
    pme_out = schemas.PmeOut(**pme_data)

    return pme_out
   
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
     
@app.get('/pmes/id/{pme_id}', response_model=schemas.PmeOut, tags=['Pme'])
def get_pme(pme_id: int, db: Session = Depends(get_db)):
    # Requête pour récupérer les données de la PME avec les informations utilisateur associées
    pme = db.query(Pme).outerjoin(Utilisateur).filter(Pme.id == pme_id).first()
    
    if pme is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="L'id fourni ne correspond à aucune Pme")

    # Transformation en format approprié
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

    return pme_data



@app.get('/pmes/recherche', response_model=list[schemas.PmeOut], tags=['Pme'])
def get_pme( search_value= Optional[str], db: Session = Depends(get_db)):
    # Requête pour récupérer les données de la PME avec les informations utilisateur associées
    pme = db.query(Pme).outerjoin(Utilisateur).filter(or_(Pme.nom_pme.contains(search_value), Utilisateur.nom_prenom.contains(search_value), Utilisateur.tel.contains(search_value), Utilisateur.email.contains(search_value))).all()
    
    if pme is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Le nom fourni ne correspond à aucune Pme")

    return pme

######################################################################################################
#            Creation de compte pour les roles "menage" et "entreprise"                              #
######################################################################################################
@app.post("/client", status_code=status.HTTP_201_CREATED,response_model=Union[schemas.ClientOut, schemas.UtilisateurOut], tags=["Client"])
async def create_client(
    quartier_id: int = Form(...),
    nom_prenom: str = Form(...),
    tel: str = Form(...),
    genre: str = Form(...),
    email: str = Form(...),
    mot_de_passe: str = Form(...),
    copie_pi: UploadFile = File(...),
    role: str = Form(...),
    create_at: datetime = Form(...),
    update_at: datetime = Form(...),
    is_actif: bool = Form(...),
    num_rccm: Optional[str] = Form(None),
    nom_entreprise: Optional[str] = Form(None),
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

    # Hasher le mot de passe
    hashed_password = hash_password(mot_de_passe)

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
        mot_de_passe=hashed_password,
        copie_pi=copie_pi_file_name,
        role=role,
        create_at=create_at,
        is_actif=is_actif,
        update_at=update_at,
    )
    db.add(db_utilisateur)
    db.commit()
    db.refresh(db_utilisateur)

    # Vérifier si le role est 'entreprise' et stocker les informations dans la table 'clients'
    if role == "entreprise" and nom_entreprise:
        db_client = Client(
            utilisateur_id=db_utilisateur.id,
            num_rccm=num_rccm,
            nom_entreprise=nom_entreprise
        )
        db.add(db_client)
        db.commit()
        db.refresh(db_client)

        client_data = schemas.ClientOut(
            id=db_client.id,
            utilisateur=db_utilisateur,
            num_rccm=db_client.num_rccm,
            nom_entreprise=db_client.nom_entreprise
        )
        return client_data
    else:
        # Si le role est formater les informations de clients selon UtilisateurOut
        if role == "menage":
            user_data = schemas.UtilisateurOut(
                  id=db_utilisateur.id,
                  quartier_id=db_utilisateur.quartier_id,
                  nom_prenom=db_utilisateur.nom_prenom,
                  tel=db_utilisateur.tel,
                  genre=db_utilisateur.genre,
                  email=db_utilisateur.email,
                  copie_pi=db_utilisateur.copie_pi,
                  role=db_utilisateur.role,
                  create_at=db_utilisateur.create_at,
                  is_actif=db_utilisateur.is_actif,
                  update_at=db_utilisateur.update_at
            )
            return user_data
        else:
            raise HTTPException(
                 status_code=status.HTTP_400_BAD_REQUEST,
                 detail="Le rôle doit être 'menage' si ce n'est pas un client entreprise."
            )


######################################################################################################
#            Affichage des informations du clients                                                   #
######################################################################################################           
@app.get('/clients', response_model=List[schemas.ClientOut], tags=['Client'])
def get_clients(db: Session = Depends(get_db)):
    # Requête pour obtenir tous les utilisateurs avec une jointure externe sur Client
    utilisateurs = db.query(Utilisateur).outerjoin(Client, Client.utilisateur_id==Utilisateur.id).filter(
        or_(Utilisateur.role == "entreprise", Utilisateur.role == "menage")
    ).all()

    # Transformer les résultats en format approprié
    client_list = []
    for utilisateur in utilisateurs:
        # Vérifier s'il y a des clients associés
        client = utilisateur.clients[0] if utilisateur.clients else None
        
        client_data = schemas.ClientOut(
            id=client.id if client else utilisateur.id,
            utilisateur=schemas.UtilisateurOut(
                id=utilisateur.id,
                quartier_id=utilisateur.quartier_id,
                nom_prenom=utilisateur.nom_prenom,
                tel=utilisateur.tel,
                genre=utilisateur.genre,
                email=utilisateur.email,
                copie_pi=utilisateur.copie_pi,
                role=utilisateur.role,
                create_at=utilisateur.create_at,
                is_actif=utilisateur.is_actif,
                update_at=utilisateur.update_at,
            ),
            num_rccm=client.num_rccm if client else None,
            nom_entreprise=client.nom_entreprise if client else None
        )
        client_list.append(client_data)

    return client_list


######################################################################################################
#                     Affichage des informations du clients                                          #
###################################################################################################### 
@app.get('/clients/{client_role}/{client_id}', response_model=Union[schemas.ClientOut, schemas.UtilisateurOut], tags=["Client"])
def get_client(client_role: str, client_id: int, db: Session = Depends(get_db)):
    # Vérification du rôle du client
    if client_role not in ["menage", "entreprise"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez afficher que les informations concernant un client de type menage ou entreprise!"
        )

    # Requête pour récupérer les informations de l'utilisateur
    utilisateur = db.query(Utilisateur).filter(Utilisateur.id == client_id).first()

    # Si l'utilisateur n'existe pas ou si le rôle est "pme", lever une exception
    if utilisateur is None or utilisateur.role != client_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun client ne correspond à vos paramètres de recherches"
        )

    # Si le rôle est "entreprise", joindre avec la table Client
    if client_role == "entreprise":
        client = db.query(Client).filter(Client.utilisateur_id == utilisateur.id).first()

        if client is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aucun client ne correspond à vos paramètres de recherches"
            )

        return schemas.ClientOut(
            id=client.id,
            utilisateur=schemas.UtilisateurOut(
                id=utilisateur.id,
                quartier_id=utilisateur.quartier_id,
                nom_prenom=utilisateur.nom_prenom,
                tel=utilisateur.tel,
                genre=utilisateur.genre,
                email=utilisateur.email,
                copie_pi=utilisateur.copie_pi,
                role=utilisateur.role,
                create_at=utilisateur.create_at,
                is_actif=utilisateur.is_actif,
                update_at=utilisateur.update_at,
            ),
            num_rccm=client.num_rccm,
            nom_entreprise=client.nom_entreprise
        )

    # Pour les rôles autres que "entreprise", retourner uniquement les informations utilisateur
    return schemas.UtilisateurOut(
            id=utilisateur.id,
            quartier_id=utilisateur.quartier_id,
            nom_prenom=utilisateur.nom_prenom,
            tel=utilisateur.tel,
            genre=utilisateur.genre,
            email=utilisateur.email,
            copie_pi=utilisateur.copie_pi,
            role=utilisateur.role,
            create_at=utilisateur.create_at,
            is_actif=utilisateur.is_actif,
            update_at=utilisateur.update_at,
        )
    

@app.get('/clients/nom_ou_tel/{client_role}/{nom_prenom}/{nom_entreprise}/{tel}', response_model=Union[schemas.ClientOut, schemas.UtilisateurOut], tags=["Client"])
def search_client(client_role: str, search_value: str, db: Session = Depends(get_db)):
    # Vérification du rôle du client
    if client_role not in ["menage", "entreprise"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez rechercher que les informations concernant un client de type menage ou entreprise!"
        )

    # Requête pour récupérer les informations de l'utilisateur
    if client_role == "menage":
        utilisateur = db.query(Utilisateur).filter(
            or_(Utilisateur.nom_prenom.contains(search_value), Utilisateur.tel.contains(search_value))
        ).first()
    elif client_role == "entreprise":
        client = db.query(Client).join(Utilisateur).filter(
            or_(Client.nom_entreprise.contains(search_value), Utilisateur.tel.contains(search_value))
        ).first()
        
        if client:
            utilisateur = client.utilisateur

    # Si aucun utilisateur ou client n'est trouvé, lever une exception
    if not utilisateur:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun client ne correspond à vos paramètres de recherches"
        )

    # Si le rôle est "entreprise", retourner les informations du client entreprise
    if client_role == "entreprise" and client:
        return schemas.ClientOut(
            id=client.id,
            utilisateur=schemas.UtilisateurOut(
                id=utilisateur.id,
                quartier_id=utilisateur.quartier_id,
                nom_prenom=utilisateur.nom_prenom,
                tel=utilisateur.tel,
                genre=utilisateur.genre,
                email=utilisateur.email,
                copie_pi=utilisateur.copie_pi,
                role=utilisateur.role,
                create_at=utilisateur.create_at,
                is_actif=utilisateur.is_actif,
                update_at=utilisateur.update_at,
            ),
            num_rccm=client.num_rccm,
            nom_entreprise=client.nom_entreprise
        )

    # Pour les rôles autres que "entreprise", retourner uniquement les informations utilisateur
    return schemas.UtilisateurOut(
            id=utilisateur.id,
            quartier_id=utilisateur.quartier_id,
            nom_prenom=utilisateur.nom_prenom,
            tel=utilisateur.tel,
            genre=utilisateur.genre,
            email=utilisateur.email,
            copie_pi=utilisateur.copie_pi,
            role=utilisateur.role,
            create_at=utilisateur.create_at,
            is_actif=utilisateur.is_actif,
            update_at=utilisateur.update_at,
        )
    
    
######################################################################################################
#                    Authentification                                                                #
###################################################################################################### 
@app.post('/login', tags=["Authentification"])
def login_user(user_access: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(Utilisateur).filter(Utilisateur.email == user_access.username).first()
    
    if not user :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Les accès fournis sont incorrects"
        )
    
    if not verify_password(user_access.password, user.mot_de_passe):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Le mot de passe fourni n'est pas le bon"
        )
    access_token = create_access_token(data={"user_id":user.id, "role":user.role})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

######################################################################################################
#                     creation d'un abonnement                                                       #
######################################################################################################
@app.post("/abonnement", response_model=schemas.AbonnementOut, tags=["Abonnement"])
async def create_abonnement(
    abonnement: schemas.AbonnementCreate,
    current_user: schemas.UtilisateurOut = Depends(role_required(["menage", "entreprise"])),
    db: Session = Depends(get_db)
):
    # Si l'utilisateur a le rôle "entreprise", vérifier qu'il est dans la table client
    if current_user.role == "entreprise":
        client = db.query(Client).filter(Client.utilisateur_id == current_user.id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="L'utilisateur entreprise n'est pas enregistré comme client."
            )

    # Créer l'abonnement
    new_abonnement = Abonnement(
        utilisateurs_id=current_user.id,
        pme_id=abonnement.pme_id,
        num_abonnement=abonnement.num_abonnement,
        tarif_abonnement=abonnement.tarif_abonnement,
        status_abonnement=abonnement.status_abonnement,
        debut_abonnement=abonnement.debut_abonnement,
        fin_abonnement=abonnement.fin_abonnement,
    )

    db.add(new_abonnement)
    db.commit()
    db.refresh(new_abonnement)

    return new_abonnement

@app.get("/pmes/{pme_id}/clients", response_model=List[Union[schemas.ClientOut, schemas.UtilisateurOut]])
def read_clients_by_pme(pme_id: int, db: Session = Depends(get_db)):
    abonnements = db.query(Abonnement).join(Client, Abonnement.client_id==Client.id).filter(Abonnement.pme_id == pme_id).all()
    if not abonnements:
        raise HTTPException(status_code=404, detail="Aucun abonnement trouvé pour cette PME")
    
    return abonnements




