import requests
import time

def test_backend_health():
    max_retries = 3
    retry_delay = 2  # saniye
    
    for attempt in range(max_retries):
        try:
            print(f"\nDeneme {attempt + 1}/{max_retries}")
            print("Backend sağlık kontrolü yapılıyor...")
            
            # Backend'in ana sayfasını kontrol et
            response = requests.get("http://localhost:8000/")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            # Swagger dokümantasyonunu kontrol et
            response = requests.get("http://localhost:8000/docs")
            print(f"\nSwagger Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("\n✅ Backend çalışıyor!")
                return True
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Backend'e bağlanılamadı! (Deneme {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                print(f"{retry_delay} saniye bekleniyor...")
                time.sleep(retry_delay)
            continue
            
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {str(e)}")
            return False
    
    print("\n❌ Backend'e bağlanılamadı! Lütfen backend'in çalıştığından emin olun.")
    return False

if __name__ == "__main__":
    test_backend_health() 