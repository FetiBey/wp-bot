from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime
from .database import Base
from datetime import datetime

class Ilan(Base):
    __tablename__ = "emlak_ilanlar"

    id = Column(Integer, primary_key=True, index=True)
    baslik = Column(String(255), index=True)
    aciklama = Column(Text)
    fiyat = Column(Float, nullable=True)
    mahalle = Column(String(255))
    sokak = Column(String(255))
    oda_sayisi = Column(String(50))
    metrekare = Column(Float, nullable=True)
    drive_link = Column(String(255), nullable=True)

class PhotoUploadSession(Base):
    __tablename__ = "photo_upload_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    expected_photos = Column(Integer)
    received_photos = Column(Integer, default=0)
    drive_folder_id = Column(String)
    photo_links = Column(JSON, default=list)
    state = Column(String, default="waiting_for_photos")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 