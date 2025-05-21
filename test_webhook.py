# test_webhook.py

import requests

# Webhook adresi
url = "http://127.0.0.1:8000/webhook"

# Twilio'nun gönderdiği gibi form verisi oluştur
data = {
    "From": "+905555555555",
    "Body": "Merhaba, yeni ilan eklemek istiyorum."
}

# POST isteği gönder
response = requests.post(url, data=data)

# Sunucudan gelen cevabı yazdır
print("Sunucudan gelen cevap:")
print(response.status_code)
print(response.text)
