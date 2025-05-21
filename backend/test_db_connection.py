from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Veritabanı URL'si: {DATABASE_URL}")

try:
    # Veritabanı bağlantısını oluştur
    engine = create_engine(DATABASE_URL)
    
    # Bağlantıyı test et
    with engine.connect() as connection:
        # Basit bir sorgu çalıştır
        result = connection.execute(text("SELECT 1"))
        print("✅ Veritabanı bağlantısı başarılı!")
        
        # Emlak ofisi tablosunu kontrol et
        result = connection.execute(text("SELECT * FROM emlak_ofisi"))
        emlak_ofisleri = result.fetchall()
        print(f"\nEmlak ofisleri ({len(emlak_ofisleri)} adet):")
        for ofis in emlak_ofisleri:
            print(f"- ID: {ofis[0]}, İsim: {ofis[1]}, Adres: {ofis[2]}, Telefon: {ofis[3]}")
        
        # İlan tablosunu kontrol et
        result = connection.execute(text("SELECT * FROM ilan"))
        ilanlar = result.fetchall()
        print(f"\nİlanlar ({len(ilanlar)} adet):")
        for ilan in ilanlar:
            print(f"- ID: {ilan[0]}, Başlık: {ilan[1]}, Fiyat: {ilan[3]}")
        
        # Foto tablosunu kontrol et
        result = connection.execute(text("SELECT * FROM foto"))
        fotolar = result.fetchall()
        print(f"\nFotoğraflar ({len(fotolar)} adet):")
        for foto in fotolar:
            print(f"- ID: {foto[0]}, İlan ID: {foto[1]}, URL: {foto[2]}")
            
except Exception as e:
    print(f"❌ Hata: {str(e)}") 