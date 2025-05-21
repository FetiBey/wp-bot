import requests
import json

# Test verisi
test_data = {
    "baslik": "Test İlanı",
    "aciklama": "Test açıklama",
    "fiyat": 2500000,
    "emlak_ofisi_id": 1,
    "konum": "Kadıköy",
    "sokak": "Moda Caddesi",
    "oda_sayisi": "3+1",
    "metrekare": "150",
    "fotolar": [
        {"url": "https://example.com/test1.jpg"},
        {"url": "https://example.com/test2.jpg"}
    ],
    "drive_folder_id": "test_folder_id"
}

# Backend API adresi
BACKEND_API_URL = "http://localhost:8000/ilan"

try:
    # POST isteği gönder
    print("Backend'e istek gönderiliyor...")
    print(f"Gönderilen veri: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
    
    response = requests.post(BACKEND_API_URL, json=test_data)
    
    # Yanıtı yazdır
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")
    
    # Başarılı ise
    if response.status_code == 200:
        print("\n✅ Test başarılı! İlan veritabanına kaydedildi.")
        
        # Kaydedilen ilanı kontrol et
        print("\nKaydedilen ilanı kontrol etmek için GET isteği gönderiliyor...")
        get_response = requests.get(BACKEND_API_URL)
        print(f"GET Response: {get_response.text}")
    else:
        print(f"\n❌ Test başarısız! Hata kodu: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ Backend'e bağlanılamadı! Backend'in çalıştığından emin olun.")
except Exception as e:
    print(f"❌ Beklenmeyen hata: {str(e)}") 