from fastapi import  Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from typing import List
from models import *
from database import get_db
from schemas import *
from utils import *

router = APIRouter(
    prefix="/calendrier",
    tags=["CalRonde"]
)

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter()

@router.post("/{utilisateur_id}", response_model=CalRondeOut, tags=["calendrier"])
async def create_calendrier(
    utilisateur_id: int,
    calrondes: CalRondeIn,
    current_user: UtilisateurOut = Depends(role_required(["pme"])),
    db: Session = Depends(get_db)
):
    # Vérification du rôle de l'utilisateur
    if current_user.role != "pme":
        raise HTTPException(status_code=403, detail="Désolé ! Vous n'êtes pas habilité(e) à accéder à ces informations.")

    # Récupération de la PME associée à l'utilisateur courant
    pme_associee = db.query(Pme).filter(Pme.utilisateur_id == current_user.id).first()

    # Vérification de l'abonnement de l'utilisateur
    abonnement = db.query(Abonnement).filter(
        Abonnement.utilisateur_id == utilisateur_id,
        Abonnement.pme_id == pme_associee.id
    ).first()

    if not abonnement:
        raise HTTPException(status_code=403, detail="Vous ne pouvez accéder qu'aux utilisateurs abonnés à votre PME.")

    # Création d'une nouvelle entrée dans CalRonde
    new_calronde = CalRonde(  # Changer CalRondeIn en CalRondeDB ici pour ajouter à la base de données
        utilisateur_id=utilisateur_id,  # Ajout de l'utilisateur_id
        pme_id=calrondes.pme_id,
        jour_passage=calrondes.jour_passage,
        heure_passage=calrondes.heure_passage,
        date_creation=datetime.now(),
        date_maj=datetime.now()
    )

    db.add(new_calronde)
    db.commit()
    db.refresh(new_calronde)

    return CalRondeOut(jour_passage=new_calronde.jour_passage, heure_passage=new_calronde.heure_passage)
