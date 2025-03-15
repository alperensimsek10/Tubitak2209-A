import pandas as pd

# Dosya yolunu belirtin
file_path = ""

# Excel dosyasını okuma
df = pd.read_excel(file_path)

# ReviewDate sütununu ay ve yıl olarak ayırma
df[['review_month', 'review_year']] = df['ReviewDate'].str.split(" ", expand=True)

# Türkçe ay isimlerini tam hale getirme
ay_cevir = {
    "Oca": "Ocak", "Şub": "Şubat", "Mar": "Mart", "Nis": "Nisan", "May": "Mayıs", "Haz": "Haziran",
    "Tem": "Temmuz", "Ağu": "Ağustos", "Eyl": "Eylül", "Eki": "Ekim", "Kas": "Kasım", "Ara": "Aralık"
}
df["review_month"] = df["review_month"].map(ay_cevir)

# Yeni dosya yolunu belirleme
new_file_path = ""

# Düzenlenmiş veriyi yeni bir Excel dosyasına kaydetme
df.to_excel(new_file_path, index=False)

print(f"Düzenlenmiş dosya kaydedildi: {new_file_path}")
