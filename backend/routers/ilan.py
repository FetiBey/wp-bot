# backend/routers/ilan.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend import crud, schemas
import logging

# Loglama ayarları
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[schemas.Ilan])
def get_ilanlar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Tüm ilanları getir"""
    ilanlar = crud.get_ilanlar(db, skip=skip, limit=limit)
    return ilanlar

@router.post("/", response_model=schemas.Ilan)
def create_ilan(ilan: schemas.IlanCreate, db: Session = Depends(get_db)):
    """Yeni ilan oluştur"""
    return crud.create_emlak_ilan(db=db, ilan=ilan)

@router.get("/{ilan_id}", response_model=schemas.Ilan)
def get_ilan(ilan_id: int, db: Session = Depends(get_db)):
    """ID'ye göre ilan getir"""
    db_ilan = crud.get_ilan(db, ilan_id=ilan_id)
    if db_ilan is None:
        raise HTTPException(status_code=404, detail="İlan bulunamadı")
    return db_ilan
