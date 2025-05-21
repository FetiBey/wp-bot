# backend/schemas/ilan.py

from pydantic import BaseModel
from typing import Optional, List

class FotoSchema(BaseModel):
    url: str

    class Config:
        from_attributes = True

class IlanBase(BaseModel):
    baslik: str
    aciklama: str
    fiyat: Optional[float] = None
    mahalle: str
    sokak: str
    oda_sayisi: str
    metrekare: Optional[float] = None
    drive_link: Optional[str] = None

class IlanCreate(IlanBase):
    pass

class Ilan(IlanBase):
    id: int

    class Config:
        from_attributes = True

class IlanResponse(BaseModel):
    id: int
    baslik: str
    aciklama: Optional[str] = None
    fiyat: Optional[float] = None
    mahalle: str
    sokak: str
    oda_sayisi: str
    metrekare: Optional[float] = None
    drive_link: Optional[str] = None

    class Config:
        from_attributes = True
