import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv
import mimetypes

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_drive_service():
    creds = None
    creds_path = os.getenv("GOOGLE_DRIVE_CREDENTIALS_FILE")

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def get_or_create_folder(service, folder_name, parent_id=None):
    # Klasör var mı kontrol et
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    if items:
        return items[0]  # Tüm folder nesnesini döndür
    
    # Yoksa oluştur
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        folder_metadata['parents'] = [parent_id]
    folder = service.files().create(body=folder_metadata, fields='id, name').execute()
    return folder  # Tüm folder nesnesini döndür

def upload_file_to_drive(filepath, filename, parent_folder_id=None):
    service = get_drive_service()

    file_metadata = {'name': filename}
    if parent_folder_id:
        file_metadata['parents'] = [parent_folder_id]
    mimetype, _ = mimetypes.guess_type(filepath)
    if mimetype is None:
        mimetype = 'application/octet-stream'  # fallback

    media = MediaFileUpload(filepath, mimetype=mimetype)

    # Dosyayı Drive'a yükle
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    file_id = file.get('id')

    # Dosyanın paylaşımını "herkese açık" yap
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(fileId=file_id, body=permission).execute()

    # Doğrudan erişilebilir link üret
    return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

def upload_multiple_photos(folder_path: str, parent_folder_id: str = None) -> list:
    """Klasördeki tüm fotoğrafları Drive'a yükle"""
    service = get_drive_service()
    photo_links = []
    
    # Klasör yolunu normalize et
    folder_path = os.path.normpath(folder_path)
    print(f"Yükleme klasörü: {folder_path}")
    
    # Klasörün var olduğunu kontrol et
    if not os.path.exists(folder_path):
        print(f"HATA: Klasör bulunamadı: {folder_path}")
        return photo_links
        
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Yüklenecek dosyalar: {files}")

    for f in files:
        full_path = os.path.join(folder_path, f)
        print(f"İşleniyor: {full_path}")
        
        if not os.path.exists(full_path):
            print(f"HATA: Dosya bulunamadı: {full_path}")
            continue
            
        file_metadata = {'name': f}
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]

        mimetype, _ = mimetypes.guess_type(full_path)
        if mimetype is None:
            mimetype = 'image/jpeg'  # varsayılan olarak jpeg

        try:
            media = MediaFileUpload(full_path, mimetype=mimetype, resumable=True)
            print(f"Dosya yükleniyor: {f}")

            # Dosyayı Drive'a yükle
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            file_id = file.get('id')
            print(f"Dosya yüklendi, ID: {file_id}")

            # Dosyanın paylaşımını "herkese açık" yap
            permission = {
                'type': 'anyone',
                'role': 'reader'
            }
            service.permissions().create(fileId=file_id, body=permission).execute()
            print(f"Dosya paylaşımı ayarlandı: {file_id}")

            # Doğrudan erişilebilir link üret
            link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
            photo_links.append({"url": link})
            print(f"Görsel başarıyla yüklendi: {f}")
        except Exception as e:
            print(f"Görsel yükleme hatası ({f}): {str(e)}")
            print(f"Hata detayı: {type(e).__name__}")
            continue

    return photo_links

def delete_folder(service, folder_name):
    """Drive'dan klasör sil"""
    try:
        # Ana klasör ID'sini .env'den al
        main_folder_id = os.getenv("GOOGLE_DRIVE_MAIN_FOLDER_ID")
        if not main_folder_id:
            raise ValueError("GOOGLE_DRIVE_MAIN_FOLDER_ID bulunamadı")

        # Klasörü ara - tam eşleşme yerine içerisinde geçen şekilde ara
        results = service.files().list(
            q=f"name contains '{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{main_folder_id}' in parents and trashed=false",
            fields="files(id, name)"
        ).execute()
        
        items = results.get('files', [])
        
        if not items:
            return False, "Klasör bulunamadı"
            
        # Eğer birden fazla sonuç varsa, tam eşleşen klasörü bul
        folder_id = None
        for item in items:
            if item['name'] == folder_name:
                folder_id = item['id']
                break
        
        if not folder_id:
            return False, "Klasör bulunamadı"
        
        # Klasörü sil
        service.files().delete(fileId=folder_id).execute()
        return True, "Klasör başarıyla silindi"
        
    except Exception as e:
        print(f"Drive klasörü silme hatası: {str(e)}")
        return False, f"Klasör silinirken hata oluştu: {str(e)}"

def get_folder_info(service, folder_name):
    """Drive'da tüm alt klasörlerde arama yapar ve tam yolunu döndürür"""
    try:
        # Sadece ana klasör altında değil, tüm drive'da arama yap
        results = service.files().list(
            q=f"name contains '{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
            fields="files(id, name, parents)"
        ).execute()
        items = results.get('files', [])
        if not items:
            return False, "Klasör bulunamadı"
        # Klasörlerin parent bilgisini de döndür
        return True, items
    except Exception as e:
        print(f"Drive klasörü bilgisi alma hatası: {str(e)}")
        return False, f"Klasör bilgisi alınırken hata oluştu: {str(e)}"

def delete_folder_by_id(service, folder_id):
    """Klasörü id ile sil"""
    try:
        service.files().delete(fileId=folder_id).execute()
        return True, "Klasör başarıyla silindi"
    except Exception as e:
        print(f"Drive klasörü silme hatası: {str(e)}")
        return False, f"Klasör silinirken hata oluştu: {str(e)}"
