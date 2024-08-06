from typing import Union
from fastapi import FastAPI
import time
from sqlalchemy.orm import Session
from models import *
from database import engine, SessionLocal, get_db, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def index_root():
    return {"message": "Bienvenue sur l'interface de developpement de conakry ville propre"}