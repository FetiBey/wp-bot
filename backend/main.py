# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import ilan
from backend.database import engine
from backend import models
import os

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Emlak API")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://real-estate-wp-gpt-bot-1.onrender.com"],  # Yeni frontend Render URL'sine izin ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(ilan.router, prefix="/ilan", tags=["ilanlar"])

# Port yapılandırması
port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
