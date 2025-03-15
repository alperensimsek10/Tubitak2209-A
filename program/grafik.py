import pandas as pd
import matplotlib.pyplot as plt

# Dosya yolları
dosya_konukOtel = "KonukOtel.xlsx"
kayit_yolu = "dil_yorum_kisi_grafik.png"

# Dosyaları oku
df_konukOtel = pd.read_excel(dosya_konukOtel)

# Dillere göre konuk yorum sayısı ve otel kişi sayısını gruplama
grouped_data = df_konukOtel.groupby('language').agg({'comment_score': 'count', 'UserID': 'nunique'}).reset_index()

# Yeni sütun isimlendirme
grouped_data.columns = ['Dil', 'Konuk Yorum Sayısı', 'Otel Kişi Sayısı']

# Grafik oluştur
fig, ax = plt.subplots(figsize=(14, 8))  # Grafik boyutunu artırdım
bar_width = 0.35  # Çubuk genişliği

# Çubuk grafiği çiz
grouped_data.set_index('Dil')[['Konuk Yorum Sayısı', 'Otel Kişi Sayısı']].plot(kind='bar', ax=ax, width=bar_width, color=['#1f77b4', '#ff7f0e'])

# Sayıları çubukların üzerine yazdır
for i, (yorum, kisi) in enumerate(zip(grouped_data['Konuk Yorum Sayısı'], grouped_data['Otel Kişi Sayısı'])):
    ax.text(i - bar_width / 2, yorum + 2, str(yorum), ha='center', fontsize=12, color='black', fontweight='bold')
    ax.text(i + bar_width / 2, kisi + 2, str(kisi), ha='center', fontsize=12, color='black', fontweight='bold')

# Başlık ve etiketler
plt.title('Dillere Göre Konuk Yorum Sayısı ve Otel Kişi Sayısı', fontsize=16, fontweight='bold')
plt.xlabel('Dil', fontsize=14, fontweight='bold')
plt.ylabel('Sayı', fontsize=14, fontweight='bold')
plt.xticks(rotation=45, fontsize=12, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')
plt.legend(title='Kategoriler', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Grafiği kaydet
plt.savefig(kayit_yolu, format='png', dpi=300)

# Grafiği göster
plt.show()
