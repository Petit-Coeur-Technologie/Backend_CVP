import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from models import *
from database import engine, Base 
from schemas import *
from routers.Abonnement import router as abonnement_router
from routers.Auth import router as auth_router
from routers.Commentaire import router as commentaire_router
from routers.Otp import router as otp_router
from routers.Pmes import router as pmes_router
from routers.Viles import router as viles_router
from routers.Clients import router as client_router
from routers.Communes import router as commune_router
from routers.Quartiers import router as quartier_router
from routers.Calendrier import router as calendrier_router
from config import UPLOAD_DIRECTORY_COPIE_PI, UPLOAD_DIRECTORY_LOGO_PME 



app = FastAPI()



app.mount("/static", StaticFiles(directory="static/Uploads"), name="uploads")
# dossiers de destination pour les uploads


# Verifier l'existence des dossiers
os.makedirs(UPLOAD_DIRECTORY_COPIE_PI, exist_ok=True)
os.makedirs(UPLOAD_DIRECTORY_LOGO_PME, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(abonnement_router)
app.include_router(auth_router)
app.include_router(commentaire_router)
app.include_router(otp_router)
app.include_router(pmes_router)
app.include_router(viles_router)
app.include_router(client_router)
app.include_router(commune_router)
app.include_router(quartier_router)
app.include_router(calendrier_router)


Base.metadata.create_all(bind=engine)


@app.get('/')
def index_root():
    return {"message": "Bienvenue sur l'interface de developpement de conakry ville propre"}







   






     





    




