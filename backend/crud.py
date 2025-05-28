from sqlalchemy.orm import Session
from . import models, schemas
from .models import Ilan, PhotoUploadSession
from .schemas.ilan import IlanCreate, PhotoUploadSessionCreate

def get_ilanlar(db: Session, skip: int = 0, limit: int = 100):
    """Tüm ilanları getir"""
    return db.query(models.Ilan).offset(skip).limit(limit).all()

def get_ilan(db: Session, ilan_id: int):
    """ID'ye göre ilan getir"""
    return db.query(models.Ilan).filter(models.Ilan.id == ilan_id).first()

def create_emlak_ilan(db: Session, ilan: schemas.IlanCreate):
    """Yeni ilan oluştur"""
    db_ilan = models.Ilan(
        baslik=ilan.baslik,
        aciklama=ilan.aciklama,
        fiyat=ilan.fiyat,
        mahalle=ilan.mahalle,
        sokak=ilan.sokak,
        oda_sayisi=ilan.oda_sayisi,
        metrekare=ilan.metrekare,
        drive_link=ilan.drive_link
    )
    db.add(db_ilan)
    db.commit()
    db.refresh(db_ilan)
    return db_ilan 

def delete_emlak_ilan(db: Session, folder_name: str):
    """İlanı veritabanından sil (başlıkta esnek arama)"""
    try:
        # Klasör adındaki #SADEEVIM ve sonrasını temizle
        base_name = folder_name.split(' #')[0].strip()
        # Başlığın baş kısmı ile eşleşen ilk ilanı bul
        ilan = db.query(models.Ilan).filter(models.Ilan.baslik.like(f"%{base_name}%")).first()
        if not ilan:
            return False, "İlan bulunamadı"
        db.delete(ilan)
        db.commit()
        return True, "İlan başarıyla silindi"
    except Exception as e:
        db.rollback()
        return False, f"İlan silinirken hata oluştu: {str(e)}" 

def create_photo_upload_session(db: Session, session_data: PhotoUploadSessionCreate):
    db_session = PhotoUploadSession(**session_data.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_photo_upload_session(db: Session, user_id: str):
    return db.query(PhotoUploadSession).filter(PhotoUploadSession.user_id == user_id).first()

def update_photo_upload_session(db: Session, user_id: str, **kwargs):
    session = db.query(PhotoUploadSession).filter(PhotoUploadSession.user_id == user_id).first()
    if session:
        for key, value in kwargs.items():
            setattr(session, key, value)
        db.commit()
        db.refresh(session)
    return session

def delete_photo_upload_session(db: Session, user_id: str):
    session = db.query(PhotoUploadSession).filter(PhotoUploadSession.user_id == user_id).first()
    if session:
        db.delete(session)
        db.commit()
    return session 