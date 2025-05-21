# Emlak İlan Botu ve Web Arayüzü

Bu proje, WhatsApp üzerinden emlak ilanlarını otomatik olarak toplayan, Google Drive'a fotoğrafları yükleyen ve modern bir web arayüzünde listeleyen bir sistemdir.

## 🚀 Özellikler

### WhatsApp Bot
- `/ekle` komutu ile yeni ilan ekleme
- GPT destekli ilan detayları analizi
- Otomatik fotoğraf toplama ve Google Drive'a yükleme
- İlanları veritabanına kaydetme

### Web Arayüzü
- Modern ve responsive tasarım
- İlanları kart görünümünde listeleme
- Gelişmiş arama ve filtreleme özellikleri
  - Başlık, açıklama ve mahalle bazında arama
  - Fiyat aralığına göre filtreleme
  - Oda sayısına göre filtreleme
  - Metrekare aralığına göre filtreleme
- Google Drive entegrasyonu ile fotoğraf görüntüleme

## 🛠️ Teknolojiler

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Twilio API (WhatsApp entegrasyonu)
- Google Drive API
- OpenAI GPT API

### Frontend
- React
- Tailwind CSS
- Axios
- Heroicons

## 📋 Gereksinimler

- Python 3.8+
- Node.js 14+
- PostgreSQL
- Google Cloud Platform hesabı
- Twilio hesabı
- OpenAI API anahtarı

## 🔧 Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/kullaniciadi/emlak-bot-yapayzeka.git
cd emlak-bot-yapayzeka
```

2. Backend bağımlılıklarını yükleyin:
```bash
pip install -r requirements.txt
```

3. Frontend bağımlılıklarını yükleyin:
```bash
cd frontend
npm install
```

4. Gerekli ortam değişkenlerini ayarlayın:
```bash
# .env dosyası oluşturun
cp .env.example .env
```

`.env` dosyasını düzenleyin:
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/emlak_db

# Twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_phone_number

# Google Drive
GOOGLE_DRIVE_CREDENTIALS_FILE=path/to/credentials.json
GOOGLE_DRIVE_MAIN_FOLDER_ID=your_folder_id

# OpenAI
OPENAI_API_KEY=your_api_key
```

5. Veritabanını oluşturun:
```bash
# PostgreSQL'de veritabanı oluşturun
createdb emlak_db

# Migrasyonları çalıştırın
alembic upgrade head
```

6. Uygulamayı başlatın:

Backend:
```bash
uvicorn bot.webhook:app --reload
```

Frontend:
```bash
cd frontend
npm start
```

## 📱 Kullanım

### WhatsApp Bot Kullanımı

1. WhatsApp'ta bot numarasına mesaj gönderin
2. `/ekle` komutunu kullanın
3. İlan detaylarını girin (örnek):
```
3+1 daire, 120m2, Bahçelievler mahallesi, 2.500.000 TL
```
4. Fotoğraf sayısını belirtin
5. Fotoğrafları gönderin

### Web Arayüzü Kullanımı

1. Tarayıcıda `http://localhost:3000` adresine gidin
2. İlanları görüntüleyin
3. Arama ve filtreleme özelliklerini kullanın
4. İlan detaylarını görüntülemek için "Detayları Gör" butonuna tıklayın

## 🤝 Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

muhammetenesdemirkol.com