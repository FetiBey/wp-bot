from sqlalchemy import Column, Integer, String, Float, Text
from .database import Base

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