import pandas as pd
import matplotlib.pyplot as plt

# Dosya yolu (Windows formatında)
file_path = ""

# Excel dosyasını oku
df = pd.read_excel(file_path)

# Sentiment değerlerini say ve yüzdelik olarak hesapla
sentiment_counts = df["hotel_sentiment"].value_counts(normalize=True) * 100

# Grafik oluştur
plt.figure(figsize=(8, 6))  # Daha büyük bir grafik boyutu
bars = sentiment_counts.plot(kind="bar", color=["red", "gray", "green"])

# Eksen başlıklarını ve grafik başlığını ayarla
plt.xlabel("Duygu Durumu", fontsize=14, fontweight="bold")
plt.ylabel("Yüzde (%)", fontsize=13, fontweight="bold")
plt.title("Otel Duygu Dağılımı", fontsize=16, fontweight="bold")
plt.xticks(rotation=0, fontsize=12)
plt.yticks(fontsize=12)

# Yüzdeleri çubukların üzerine ekleyelim
for bar in bars.patches:
    plt.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 1,
             f"%{bar.get_height():.1f}",
             ha='center', fontsize=12, fontweight="bold")

# Grafiği kaydet
plt.savefig("sentiment_distribution.png", dpi=300, bbox_inches="tight")
plt.show()
