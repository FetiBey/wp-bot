import sys
import os
import requests
from requests.auth import HTTPBasicAuth
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import json
from twilio.rest import Client
from sqlalchemy.orm import Session
from googleapiclient.errors import HttpError
import re
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from bot.gpt_parser import parse_message_to_json
from drive_service.uploader import upload_multiple_photos, upload_file_to_drive, get_or_create_folder, get_drive_service, delete_folder, get_folder_info, delete_folder_by_id
from backend.database import SessionLocal
from backend.crud import create_emlak_ilan, get_ilanlar, delete_emlak_ilan, create_photo_upload_session, get_photo_upload_session, update_photo_upload_session, delete_photo_upload_session
from backend.schemas.ilan import IlanCreate, PhotoUploadSessionCreate

load_dotenv()

app = FastAPI()

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React uygulamasının çalıştığı adres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Backend API adresi
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/ilan")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Twilio client oluştur
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Kullanıcı durumlarını takip etmek için sözlük
user_states = {}

def generate_ilan_baslik(mahalle, sokak, oda_sayisi):
    mahalle = ''.join(c for c in mahalle if c.isalnum() or c.isspace())
    sokak = ''.join(c for c in sokak if c.isalnum() or c.isspace())
    return f"{mahalle}-{sokak}-{oda_sayisi}"

def create_ilan_folder(service, ilan_details):
    """İlan için Drive'da klasör oluştur"""
    try:
        # Ana klasör ID'sini .env'den al
        main_folder_id = os.getenv("GOOGLE_DRIVE_MAIN_FOLDER_ID")
        if not main_folder_id:
            raise ValueError("GOOGLE_DRIVE_MAIN_FOLDER_ID bulunamadı")

        # İlan detaylarını al
        mahalle = ilan_details.get("mahalle", "Belirsiz")
        sokak = ilan_details.get("sokak", "Belirsiz")
        oda_sayisi = ilan_details.get("oda_sayisi", "Belirsiz")
        
        # İlan klasör adını oluştur
        ilan_folder_name = generate_ilan_baslik(mahalle, sokak, oda_sayisi) + " #SADEEVIM"
        
        # 3+1 kontrolü
        if oda_sayisi.strip().lower() == "3 + 1":
            # Doğrudan ana klasöre ekle
            parent_id = main_folder_id
        else:
            # Önce oda türü klasörünü oluştur veya bul
            oda_folder_name = oda_sayisi.strip()
            oda_folder = get_or_create_folder(service, oda_folder_name, main_folder_id)
            parent_id = oda_folder.get('id')
        
        # İlan klasörünü oluştur
        folder_metadata = {
            'name': ilan_folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')
        
        # Klasörü herkese açık yap
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        service.permissions().create(fileId=folder_id, body=permission).execute()
        
        print(f"Drive klasörü oluşturuldu. ID: {folder_id}")
        return folder_id
    except Exception as e:
        print(f"Drive klasörü oluşturma hatası: {str(e)}")
        print(f"Hata detayı: {type(e).__name__}")
        raise

def send_whatsapp_message(to_number: str, message: str):
    """WhatsApp mesajı gönder"""
    try:
        message = twilio_client.messages.create(
            from_=f"whatsapp:{TWILIO_PHONE_NUMBER}",
            body=message,
            to=to_number
        )
        print(f"WhatsApp mesajı gönderildi: {message.sid}")
        return True
    except Exception as e:
        print(f"WhatsApp mesajı gönderme hatası: {str(e)}")
        return False

def process_ilan(from_number: str, ilan_details: dict, drive_folder_id: str):
    """İlanı işle ve veritabanına kaydet"""
    try:
        # Drive klasör linkini oluştur
        drive_link = f"https://drive.google.com/drive/folders/{drive_folder_id}"
        
        # Veritabanına kaydet
        db = SessionLocal()
        try:
            # Metrekare değerini float'a çevir
            metrekare = ilan_details.get("metrekare", "")
            try:
                metrekare = float(metrekare) if metrekare else None
            except ValueError:
                metrekare = None

            # Fiyat değerini float'a çevir
            fiyat = ilan_details.get("fiyat", "")
            try:
                fiyat = float(fiyat) if fiyat else None
            except ValueError:
                fiyat = None

            # IlanCreate nesnesi oluştur
            mahalle = ilan_details.get("mahalle", "")
            sokak = ilan_details.get("sokak", "")
            oda_sayisi = ilan_details.get("oda_sayisi", "")
            baslik = generate_ilan_baslik(mahalle, sokak, oda_sayisi)
            ilan_data = IlanCreate(
                baslik=baslik,
                aciklama=ilan_details.get("aciklama", ""),
                fiyat=fiyat,
                mahalle=mahalle,
                sokak=sokak,
                oda_sayisi=oda_sayisi,
                metrekare=metrekare,
                drive_link=drive_link
            )
            
            db_ilan = create_emlak_ilan(db, ilan_data)
            
            # Kullanıcıya bildirim gönder
            success_message = f"İlanınız başarıyla kaydedildi!\n\nDrive klasör linki: {drive_link}"
            send_whatsapp_message(from_number, success_message)
            
            return True
        finally:
            db.close()
    except Exception as e:
        print(f"İlan işleme hatası: {str(e)}")
        error_message = "İlan kaydedilirken bir hata oluştu. Lütfen daha sonra tekrar deneyiniz."
        send_whatsapp_message(from_number, error_message)
        return False

@app.post("/webhook")
async def receive_message(request: Request):
    try:
        form_data = await request.form()
        from_number = form_data.get("From")
        message_body = form_data.get("Body")
        num_media = int(form_data.get("NumMedia", 0))

        print(f"\nYeni mesaj geldi: {from_number} - {message_body} (Foto sayısı: {num_media})")
        print(f"Form verileri: {dict(form_data)}")
        print(f"Mevcut kullanıcı durumu: {json.dumps(user_states.get(from_number, {}), indent=2)}")

        # TwiML yanıtı oluştur
        resp = MessagingResponse()

        # Kullanıcının mevcut durumunu kontrol et
        current_state = user_states.get(from_number, {})

        if message_body and message_body.strip().lower() == "/tamamla":
            if current_state.get("state") == "waiting_for_photos":
                # İlanı tamamla
                db = SessionLocal()
                try:
                    session = get_photo_upload_session(db, from_number)
                    if not session:
                        resp.message("Önce ilan detaylarını girmeniz gerekiyor.")
                        response = Response(content=str(resp), media_type="application/xml")
                        return response

                    if session.received_photos == 0:
                        resp.message("En az bir fotoğraf eklemeniz gerekiyor.")
                        response = Response(content=str(resp), media_type="application/xml")
                        return response

                    if process_ilan(from_number, current_state["details"], session.drive_folder_id):
                        # Drive klasör linkini oluştur
                        drive_link = f"https://drive.google.com/drive/folders/{session.drive_folder_id}"
                        delete_photo_upload_session(db, from_number)
                        user_states[from_number] = {}
                        resp.message(f"İlanınız başarıyla kaydedildi!\n\nDrive klasör linki: {drive_link}")
                    else:
                        resp.message("İlan kaydedilirken bir hata oluştu. Lütfen tekrar deneyiniz.")
                finally:
                    db.close()
            else:
                resp.message("Önce ilan detaylarını girmeniz gerekiyor.")
            response = Response(content=str(resp), media_type="application/xml")
            return response

        elif message_body and message_body.strip().lower() == "/sil":
            # Silme işlemi için kullanıcıdan anahtar kelime iste
            user_states[from_number] = {
                "state": "waiting_for_search_keyword",
                "action": "delete"
            }
            resp.message("Lütfen silmek istediğiniz klasör için bir anahtar kelime (ör: mahalle, oda tipi, vs.) giriniz.")
            response = Response(content=str(resp), media_type="application/xml")
            return response

        elif current_state.get("state") == "waiting_for_search_keyword" and current_state.get("action") == "delete":
            search_keyword = message_body.strip()
            drive_service = get_drive_service()
            success, folder_info = get_folder_info(drive_service, search_keyword)
            if not success:
                resp.message(f"Klasör bulunamadı. Lütfen anahtar kelimeyi kontrol ediniz.")
                response = Response(content=str(resp), media_type="application/xml")
                return response

            # Klasörlerin tam yolunu bulmak için yardımcı fonksiyon
            def get_folder_path(service, folder_id, name_cache=None):
                if name_cache is None:
                    name_cache = {}
                try:
                    folder = service.files().get(fileId=folder_id, fields="id, name, parents").execute()
                    name = folder['name']
                    parents = folder.get('parents', [])
                    if not parents:
                        return name
                    parent_id = parents[0]
                    if parent_id in name_cache:
                        parent_name = name_cache[parent_id]
                    else:
                        parent = service.files().get(fileId=parent_id, fields="id, name, parents").execute()
                        parent_name = parent['name']
                        name_cache[parent_id] = parent_name
                    return f"{get_folder_path(service, parent_id, name_cache)}/{name}"
                except HttpError:
                    return name

            # Klasörleri numaralandırılmış liste olarak göster
            folder_list = []
            for idx, item in enumerate(folder_info, 1):
                folder_path = get_folder_path(drive_service, item['id'])
                folder_list.append(f"{idx}. {folder_path}")

            folder_list_text = "\n".join(folder_list)
            resp.message(f"Bulunan klasörler:\n{folder_list_text}\n\nLütfen silmek istediğiniz klasörün numarasını giriniz.")
            
            # Klasör bilgilerini state'e kaydet
            user_states[from_number] = {
                "state": "waiting_for_folder_number",
                "action": "delete",
                "folder_list": folder_info
            }
            response = Response(content=str(resp), media_type="application/xml")
            return response

        elif current_state.get("state") == "waiting_for_folder_number" and current_state.get("action") == "delete":
            try:
                folder_number = int(message_body.strip())
                folder_list = current_state.get("folder_list", [])
                
                if folder_number < 1 or folder_number > len(folder_list):
                    resp.message("Geçersiz numara. Lütfen listeden bir numara seçiniz.")
                    response = Response(content=str(resp), media_type="application/xml")
                    return response

                selected_folder = folder_list[folder_number - 1]
                folder_id = selected_folder['id']

                drive_service = get_drive_service()
                # Klasörü id ile sil
                drive_success, drive_message = delete_folder_by_id(drive_service, folder_id)

                # Veritabanından ilanı sil
                db = SessionLocal()
                try:
                    # Klasör adını veritabanındaki başlık formatına çevir
                    db_folder_name = selected_folder['name'].replace(" #SADEEVIM", "").strip()
                    db_success, db_message = delete_emlak_ilan(db, db_folder_name)
                finally:
                    db.close()

                # Sonucu kullanıcıya bildir
                if drive_success and db_success:
                    resp.message("İlan ve ilgili klasör başarıyla silindi.")
                else:
                    error_message = "İlan silinirken hatalar oluştu:\n"
                    if not drive_success:
                        error_message += f"Drive: {drive_message}\n"
                    if not db_success:
                        error_message += f"Veritabanı: {db_message}"
                    resp.message(error_message)

            except ValueError:
                resp.message("Lütfen geçerli bir numara giriniz.")
                response = Response(content=str(resp), media_type="application/xml")
                return response

            # Kullanıcı durumunu sıfırla
            user_states[from_number] = {}

            response = Response(content=str(resp), media_type="application/xml")
            return response

        # Eğer kullanıcı herhangi bir durumda değilse ve mesaj gönderdiyse, ilan detaylarını analiz et
        elif not current_state:
            try:
                print(f"İlan detayları analiz ediliyor: {message_body}")
                parsed_details = parse_message_to_json(message_body)
                print(f"Analiz sonucu: {json.dumps(parsed_details, indent=2)}")
                
                if not parsed_details:
                    print("İlan detayları analiz edilemedi")
                    resp.message("İlan detayları analiz edilemedi. Lütfen daha açıklayıcı bir şekilde tekrar giriniz.")
                    response = Response(content=str(resp), media_type="application/xml")
                    print(f"Gönderilen yanıt: {str(resp)}")
                    return response
                
                # İlan detaylarını kaydet ve fotoğraf bekleme durumuna geç
                user_states[from_number] = {
                    "state": "waiting_for_photos",
                    "details": parsed_details,
                    "photos": [],
                    "temp_photos": []
                }
                print(f"İlan detayları kaydedildi: {json.dumps(parsed_details, indent=2)}")
                resp.message("İlan detayları kaydedildi. Şimdi fotoğrafları gönderebilirsiniz. İşlem bittiğinde /tamamla komutunu kullanın.")
                response = Response(content=str(resp), media_type="application/xml")
                print(f"Gönderilen yanıt: {str(resp)}")
                return response
            except Exception as e:
                print(f"İlan detayları analiz hatası: {str(e)}")
                print(f"Hata detayı: {type(e).__name__}")
                resp.message("İlan detayları analiz edilirken bir hata oluştu. Lütfen tekrar deneyiniz.")
                response = Response(content=str(resp), media_type="application/xml")
                print(f"Gönderilen yanıt: {str(resp)}")
                return response

        elif current_state.get("state") == "waiting_for_photos":
            db = SessionLocal()
            session = get_photo_upload_session(db, from_number)
            if not session:
                # İlk görsel geldiğinde session oluştur
                session_data = PhotoUploadSessionCreate(
                    user_id=from_number,
                    expected_photos=999,  # Maksimum fotoğraf sayısı
                    received_photos=0,
                    drive_folder_id=None,
                    photo_links=[],
                    state="waiting_for_photos"
                )
                session = create_photo_upload_session(db, session_data)

            if num_media > 0:
                print(f"\nYeni görseller alındı: {num_media} adet")
                import time
                if not session.drive_folder_id:
                    service = get_drive_service()
                    drive_folder_id = create_ilan_folder(service, current_state["details"])
                    update_photo_upload_session(db, from_number, drive_folder_id=drive_folder_id)
                else:
                    drive_folder_id = session.drive_folder_id

                for i in range(num_media):
                    media_url = form_data.get(f"MediaUrl{i}")
                    media_type = form_data.get(f"MediaContentType{i}")
                    ext = ".jpg" if "jpeg" in media_type else ".png"
                    try:
                        response = requests.get(media_url, auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
                        if response.status_code == 200:
                            temp_filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}{ext}"
                            with open(temp_filename, "wb") as f:
                                f.write(response.content)
                            # Drive'a yükle
                            service = get_drive_service()
                            file_link = upload_file_to_drive(temp_filename, temp_filename, drive_folder_id)
                            # Veritabanında linki güncelle
                            photo_links = session.photo_links or []
                            photo_links.append(file_link)
                            update_photo_upload_session(db, from_number, received_photos=session.received_photos+1, photo_links=photo_links)
                            print(f"Fotoğraf yüklendi: {file_link}")
                            os.remove(temp_filename)
                        else:
                            print(f"Fotoğraf indirme hatası: {response.status_code}")
                            print(f"Hata detayı: {response.text}")
                    except Exception as e:
                        print(f"Fotoğraf indirme hatası: {str(e)}")
                        print(f"Hata detayı: {type(e).__name__}")

                session = get_photo_upload_session(db, from_number)
                send_whatsapp_message(from_number, f"Fotoğraf başarıyla yüklendi. Toplam {session.received_photos} fotoğraf yüklendi. İşlem bittiğinde /tamamla komutunu kullanın.")
                db.close()
                return Response(content="", media_type="application/xml")
            else:
                print("Görsel beklenirken medya yok")
                send_whatsapp_message(from_number, "Lütfen fotoğraf gönderin veya işlemi tamamlamak için /tamamla komutunu kullanın.")
                db.close()
                return Response(content="", media_type="application/xml")

        # Varsayılan yanıt
        resp.message("İlan eklemek için ilan detaylarını giriniz. İşlem bittiğinde /tamamla komutunu kullanın.")
        return Response(content=str(resp), media_type="application/xml")

    except Exception as e:
        print(f"Genel hata: {str(e)}")
        print(f"Hata detayı: {type(e).__name__}")
        resp = MessagingResponse()
        resp.message("Bir hata oluştu. Lütfen tekrar deneyiniz.")
        return Response(content=str(resp), media_type="application/xml")

@app.get("/ilan")
async def get_ilanlar_endpoint():
    try:
        db = SessionLocal()
        try:
            ilanlar = get_ilanlar(db)
            return ilanlar
        finally:
            db.close()
    except Exception as e:
        print(f"İlanları getirme hatası: {str(e)}")
        print(f"Hata detayı: {type(e).__name__}")
        return {"error": "İlanlar getirilirken bir hata oluştu"}
