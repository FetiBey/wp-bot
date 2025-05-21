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
        result = connection.execute(text("SELECT 1"))
        print("Veritabanı bağlantısı başarılı!")
        
        # Veritabanı listesini kontrol et
        result = connection.execute(text("SELECT datname FROM pg_database"))
        databases = [row[0] for row in result]
        print(f"Mevcut veritabanları: {databases}")
        
        # Tabloları kontrol et
        result = connection.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        tables = [row[0] for row in result]
        print(f"Mevcut tablolar: {tables}")
        
except Exception as e:
    print(f"Veritabanı bağlantı hatası: {str(e)}") 