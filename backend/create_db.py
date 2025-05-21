import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from models import Base

def create_database():
    # PostgreSQL'e bağlan
    conn = psycopg2.connect(
        user="postgres",
        password="1723",
        host="localhost",
        port="5432"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    # Veritabanını oluştur
    try:
        cur.execute("CREATE DATABASE emlak_db")
        print("Veritabanı başarıyla oluşturuldu.")
    except psycopg2.Error as e:
        print(f"Veritabanı zaten mevcut veya bir hata oluştu: {e}")
    
    cur.close()
    conn.close()

def create_tables():
    # SQLAlchemy engine oluştur
    engine = create_engine(
        "postgresql://postgres:1723@localhost:5432/emlak_db",
        client_encoding='utf8'
    )
    
    # Tabloları oluştur
    Base.metadata.create_all(bind=engine)
    print("Tablolar başarıyla oluşturuldu.")

if __name__ == "__main__":
    create_database()
    create_tables() 