# api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models
from .utils import get_db
from typing import List, Optional

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Bob Ross API is running"}

@router.get("/episodes")
def get_episodes(
    db: Session = Depends(get_db),
    month: Optional[int] = None,
    color: Optional[str] = None,
    subject: Optional[str] = None
):
    query = db.query(models.Episode)
    
    if month:
        query = query.filter(models.Episode.broadcast_month == month)
    
    if color:
        query = query.join(models.Episode.colors).filter(models.Color.name.ilike(f"%{color}%"))
    
    if subject:
        query = query.join(models.Episode.subjects).filter(models.Subject.name.ilike(f"%{subject}%"))
    
    return query.all()

@router.get("/colors")
def get_colors(db: Session = Depends(get_db)):
    return db.query(models.Color).all()

@router.get("/subjects")
def get_subjects(db: Session = Depends(get_db)):
    return db.query(models.Subject).all()