from fastapi import Depends, HTTPException,status, APIRouter
from sqlalchemy.orm import Session
from typing import List
from models import *
from database import get_db
from schemas import *
from utils import *


router = APIRouter(
    prefix="/vile",
    tags=["Villes"]
   
)


@router.get("/", response_model=List[Ville], tags=["Villes"])
def get_villes(db: Session = Depends(get_db)):
    
    villes = db.query(Ville).all()
    
    return villes

@router.get("/{id}/communes", response_model=List[Commune], tags=["Villes"])
def get_com_by_villes(id: int, db: Session = Depends(get_db)):
    
    communes = db.query(Commune).filter(Commune.ville_id==id).all()
    
    return communes





