from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional, List
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import uvicorn

from database import SessionLocal, engine
import models
import schemas
from schemas import clientRepMenage, clientCreateMenage, clientRepEntreprise, clientCreateEntreprise, Token, utilisateur


# Initialiser l'application FastAPI
app = FastAPI()

# Configuration pour la sécurité des mots de passe et JWT
SECRET_KEY = "eca906e7edcfd0cf1ac5efe97a5017ce9e5f015f482c18ca4f5ea33f19119f18"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fonction pour obtenir la session de la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fonctions utilitaires pour les mots de passe et les tokens
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dépendance pour obtenir l'utilisateur actuel
def get_user_by_email(db: Session, email: str):
    return db.query(models.Utilisateur).filter(models.Utilisateur.email == email).first()

def get_user_by_nom(db: Session, nom_prenom: str):
    return db.query(models.Utilisateur).filter(models.Utilisateur.nom_prenom == nom_prenom).first()

def authenticate_user(db: Session, identifier: str, password: str):
    user = get_user_by_email(db, identifier)
    if not user:
        user = get_user_by_nom(db, identifier)
    if not user or not verify_password(password, user.mot_de_passe):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# Endpoint pour l'enregistrement d'une PME
@app.post("/register_pme", response_model=schemas.pmeRep)
def register_pme(user: schemas.pmeCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email deja existant")
    hashed_password = get_password_hash(user.mot_de_passe)
    db_user = models.Utilisateur(
        quartier_id=user.quartier_id,
        nom_prenom=user.nom_prenom,
        email=user.email,
        mot_de_passe=hashed_password,
        tel=user.tel,
        genre=user.genre,
        copie_PI=user.copie_PI,
        role="PME",
        statut_actif=user.statut_actif,
        date_inscription=datetime.now()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_pme = models.Pme(
        nom_pme=user.nom_pme,
        description=user.description,
        zone_intervention=user.zone_intervention,
        logo_pme=user.logo_pme,
        tarif_abonnement=user.tarif_abonnement,
        utilisateur_id=db_user.id
    )
    db.add(db_pme)
    db.commit()
    db.refresh(db_pme)
    return db_pme

# Endpoint pour obtenir les informations d'une PME
@app.get("/pme/{nom_prenom}", response_model=schemas.pmeRep)
def read_pme(nom_prenom: int, db: Session = Depends(get_db)):
    db_pme = db.query(models.pme).filter(models.pme.nom_prenom== nom_prenom).first()
    if db_pme is None:
        raise HTTPException(status_code=404, detail="PME non trouvee")
    return db_pme

@app.get("/client/{nom_prenom}", response_model=schemas.clientRepEntreprise)
def read_client(nom_prenom: int, db: Session = Depends(get_db)):
    db_client = db.query(models.client).filter(models.client.nom_entreprise == nom_entreprise).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="client non trouve")
    return db_client

@app.post("/inscription_client_menage", response_model=list[clientRepMenage])
def inscription_client_menage(user: clientCreateMenage, db: Session = Depends(get_db)):
    db_user = get_client_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email deja existant")

    hashed_password = get_password_hash(user.mot_de_passe)
    db_user = utilisateurs(
        quartier_id=user.quartier_id,
        nom_prenom=user.nom_prenom,
        email=user.email,
        mot_de_passe=hashed_password,
        tel=user.tel,
        genre=user.genre,
        copie_PI=user.copie_PI,
        role="client",
        statut_actif="actif",
        date_inscription=datetime.utcnow().date()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    db_client = client(
        id=db_user.id,
        utilisateur=db_user
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.post("/inscription_client_entreprise", response_model=clientRepEntreprise)
def inscription_client_entreprise(user: clientCreateEntreprise, db: Session = Depends(get_db)):
    db_user = get_client_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email deja existant")

    hashed_password = get_password_hash(user.mot_de_passe)
    db_user = utilisateurs(
        quartier_id=user.quartier_id,
        nom_prenom=user.nom_prenom,
        email=user.email,
        mot_de_passe=hashed_password,
        tel=user.tel,
        genre=user.genre,
        copie_PI=user.copie_PI,
        role="client",
        statut_actif="actif",
        date_inscription=datetime.utcnow().date()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    db_client = client(
        id=db_user.id,
        utilisateur=db_user,
        num_rccm=user.num_rccm,
        nom_entreprise=user.nom_entreprise
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# Endpoint pour la connexion
@app.post("/login", response_model= Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, identifier=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint pour obtenir les informations de l'utilisateur actuel
@app.get("/users/me", response_model=utilisateur)
async def read_users_me(current_user: utilisateur = Depends(get_current_user)):
    return current_user