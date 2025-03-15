import pandas as pd

# Dosya yolu
file_path = ""

# Dosyayı oku
df = pd.read_excel(file_path)

# Ay kısaltmalarını tam isimlere çevirmek için bir sözlük
month_map = {
    "Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April",
    "May": "May", "Jun": "June", "Jul": "July", "Aug": "August",
    "Sep": "September", "Oct": "October", "Nov": "November", "Dec": "December"
}

# joining_month sütunundaki kısaltmaları tam haline çevir
df["joining_month"] = df["joining_month"].map(month_map).fillna(df["joining_month"])

# Güncellenmiş dosyayı yeni bir isimle kaydet
updated_file_path = ""
df.to_excel(updated_file_path, index=False)

print(f"Dosya başarıyla güncellendi! ✅ Yeni dosya: {updated_file_path}")
