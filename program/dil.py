import pandas as pd
from langdetect import detect, DetectorFactory
from langcodes import Language

# Dil kodlarını Türkçe isimlere çevirmek için sözlük
turkce_dil_isimleri = {
    "en": "İngilizce",
    "tr": "Türkçe",
    "fr": "Fransızca",
    "de": "Almanca",
    "es": "İspanyolca",
    "it": "İtalyanca",
    "ru": "Rusça",
    "ar": "Arapça",
    "zh": "Çince",
    "ja": "Japonca",
    "ko": "Korece",
    "nl": "Felemenkçe",
    "pt": "Portekizce",
    "sv": "İsveççe",
    "pl": "Lehçe",
    "hi": "Hintçe"
}

# Dosyayı oku
df = pd.read_excel("")

# Dil tespitinin tutarlı olması için sabit bir durum belirleyelim
DetectorFactory.seed = 0

def detect_language(text):
    try:
        lang_code = detect(text)
        return turkce_dil_isimleri.get(lang_code, "Bilinmeyen")
    except:
        return "Bilinmeyen"

# Yeni sütunu ekleyelim
df['language'] = df['comment_text'].astype(str).apply(detect_language)

# Yeni dosyayı kaydet
df.to_excel("", index=False)

print("İşlem tamamlandı! Yeni dosya: guest_with_languages.xlsx")
