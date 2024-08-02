from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import uvicorn

# Importation des modèles SQLAlchemy et Pydantic
from models import Utilisateurs, Pme, Client
from schemas import UtilisateurCreate, Utilisateur, Token, TokenData
from database import SessionLocal, engine

# Configuration de l'application FastAPI
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
    return db.query(Utilisateurs).filter(Utilisateurs.email == email).first()

def get_pme_by_email(db: Session, email: str):
    return db.query(Utilisateurs).filter(Utilisateurs.email == email).first()

def get_pme_by_nom(db: Session, nom_prenom: str):
    return db.query(Utilisateurs).filter(Utilisateurs.nom_prenom == nom_prenom).first()

def authenticate_user(db: Session, identifier: str, password: str):
    # Essayer de récupérer l'utilisateur par email
    user = get_user_by_email(db, identifier)
    if not user:
        # Si aucun utilisateur n'est trouvé par email, essayer de récupérer par nom_prenom
        user = get_user_by_nom(db, identifier)
    if not user or not verify_password(password, user.mot_de_passe):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Exception pour les erreurs de validation des credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Décoder le token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    # Obtenir l'utilisateur à partir de l'email
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

@app.post("/register", response_model=Pme)
def register_pme(user: pmeCreate, db: Session = Depends(get_db)):
    db_user = get_pme_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email deja existant")
    hashed_password = get_password_hash(user.mot_de_passe)
    db_user = Utilisateurs(
        nom_prenom=user.nom_prenom,
        email=user.email,
        mot_de_passe=hashed_password,
        tel=user.tel,
        genre=user.genre,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
# Endpoint pour l'enregistrement
@app.post("/Inscription_client", response_model=Client)
def inscription_client(user: ClientCreateBase, db: Session = Depends(get_db)):
    db_user = get_client_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email deja existant")

    hashed_password = get_password_hash(user.mot_de_passe)

    if user.type_client == "menage":
        db_user = ClientModel(
            nom_prenom=user.nom_prenom,
            email=user.email,
            mot_de_passe=hashed_password,
            tel=user.tel,
            genre=user.genre,
            type_client=user.type_client,
            pi_client=user.pi_client
        )
    elif user.type_client == "entreprise":
        db_user = ClientModel(
            nom_prenom=user.nom_prenom,
            email=user.email,
            mot_de_passe=hashed_password,
            tel=user.tel,
            genre=user.genre,
            type_client=user.type_client,
            pi_client=user.pi_client,
            num_rccm=user.num_rccm,
            nom_entreprise=user.nom_entreprise
        )
    else:
        raise HTTPException(status_code=400, detail="Type de client invalide")

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Endpoint pour la connexion
@app.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Authentification de l'utilisateur soit par email, soit par nom
    user = authenticate_user(db, identifier=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Création du token d'accès
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint pour obtenir les informations de l'utilisateur actuel
@app.get("/users/me", response_model=Utilisateur)
async def read_users_me(current_user: Utilisateur = Depends(get_current_user)):
    return current_user

