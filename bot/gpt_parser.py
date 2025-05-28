# bot/gpt_parser.py

import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Örnek prompt fonksiyonu
def parse_message_to_json(message: str) -> dict:
    prompt = f"""
Aşağıdaki emlak mesajını analiz et ve yapılandırılmış bir JSON nesnesi olarak döndür:

Mesaj: "{message}"

Format:
{{
  "baslik": "...",
  "aciklama": "...",
  "fiyat": 0,
  "emlak_ofisi_id": 1,
  "konum": "...",  # Mahalle adı
  "sokak": "...",  # Sokak/Cadde adı
  "oda_sayisi": "...",  # 1+1, 2+1, 3+1 gibi
  "metrekare": "...",  # Varsa metrekare bilgisi
  "fotolar": []
}}

Notlar:
- "emlak_ofisi_id" alanını her zaman 1 olarak ayarla.
- "fiyat" TL cinsindedir, sadece sayı olarak yaz.
- "konum" alanına sadece mahalle adını yaz.
- "sokak" alanına sadece sokak/cadde adını yaz.
- "oda_sayisi" alanına sadece oda sayısını yaz (örn: "2+1").
- "metrekare" alanına varsa metrekare bilgisini yaz.
- JSON dışında hiçbir şey yazma.
- Eğer mesajda birden fazla satır varsa, genellikle ilk satır mahalle bilgisidir. Başındaki emoji veya işareti temizle.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    json_str = response.choices[0].message.content

    # JSON metnini Python dict'e dönüştür
    try:
        result = json.loads(json_str)
        # Eğer mahalle (konum) boşsa, ilk satırı kullan
        if not result.get('konum'):
            first_line = message.strip().split('\n')[0]
            # Başındaki emoji ve işaretleri temizle
            import re
            first_line = re.sub(r'^[^\w\d]+', '', first_line).strip()
            result['konum'] = first_line
        # Anahtar uyumluluğu: 'mahalle' anahtarını da ekle
        result['mahalle'] = result.get('konum', '')
        return result
    except Exception as e:
        print("GPT çıktısı parse edilemedi:", e)
        return {}
