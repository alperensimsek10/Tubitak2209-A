import pandas as pd
import matplotlib.pyplot as plt
import ast

# Dosya yolunu belirleme
file_path = ""

# Excel dosyasını okuma
xls = pd.ExcelFile(file_path)

# Sayfa isimlerini kontrol etme
print("Sayfa isimleri:", xls.sheet_names)

# Sayfanın içeriğini okuma
df = pd.read_excel(xls, sheet_name="Sheet1")


# Sentiment dağılımını işlemek için fonksiyon
def sentiment_percentage(comment_dist):
    sentiment_counts = {"Pozitif": 0, "Negatif": 0, "Nötr": 0}

    for dist in comment_dist.dropna():  # Boş değerleri filtrele
        dist_dict = ast.literal_eval(dist)  # Stringi dict formatına çevir
        for key in dist_dict:
            sentiment_counts[key] += dist_dict[key]

    total = sum(sentiment_counts.values())
    sentiment_percentages = {key: (value / total) * 100 for key, value in sentiment_counts.items()}
    return sentiment_percentages


# Sentiment yüzdelerini hesapla
sentiment_data = sentiment_percentage(df['comment_sentiment_distribution'])

# Grafik oluşturma (oranlarla birlikte)
plt.figure(figsize=(8, 6))
bars = plt.bar(sentiment_data.keys(), sentiment_data.values(), color=['green', 'red', 'gray'])

# Oranları çubukların üzerine yazdırma
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'%{height:.1f}',
             ha='center', va='bottom', fontsize=12, fontweight='bold')

# Başlıkları kalın yapma
plt.xlabel("Sentiment", fontsize=14, fontweight='bold')
plt.ylabel("Yüzde (%)", fontsize=14, fontweight='bold')
plt.title("Konuk Sentiment Dağılımı", fontsize=16, fontweight='bold')
plt.ylim(0, 100)

# PNG olarak kaydetme
output_path = "sentiment_analysis_with_percentages.png"
plt.savefig(output_path)

# Görüntüleme
plt.show()

print(f"Grafik kaydedildi: {output_path}")
