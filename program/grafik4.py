import pandas as pd
from textblob import TextBlob

# Dosya yolları
input_file_path = ""
output_user_file_path = ""

# Dosyayı oku
df = pd.read_excel(input_file_path)

# Sayısal verileri dönüştür (Hatalı girişleri NaN yap)
df["review_score"] = pd.to_numeric(df["review_score"], errors="coerce")

# Yorum metninden duygu analizi yapacak fonksiyon
def get_sentiment(text):
    text = str(text)  # NaN veya boş değerleri string'e çevir
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "Pozitif"
    elif polarity < 0:
        return "Negatif"
    else:
        return "Nötr"

# 'comment_text' sütunu varsa duygu analizi yap
if "comment_text" in df.columns:
    df["Yorum Duygusu"] = df["comment_text"].apply(get_sentiment)
else:
    df["Yorum Duygusu"] = "Bilinmiyor"

# Kullanıcı bazlı analiz için liste oluştur
user_data = []

# Kullanıcılara göre grupla
grouped_users = df.groupby("UserID")
for user, data in grouped_users:
    total_reviews = len(data)  # Kullanıcının yaptığı toplam yorum sayısı
    avg_user_rating = data["review_score"].mean(skipna=True)  # Kullanıcının verdiği ortalama puan
    user_sentiment = data["Yorum Duygusu"].mode()[0] if not data["Yorum Duygusu"].empty else "Bilinmiyor"  # Kullanıcının baskın duygusu

    # En çok gidilen oteli bul
    most_visited_hotel_mode = data["hotel_name"].mode()
    most_visited_hotel = most_visited_hotel_mode[0] if not most_visited_hotel_mode.empty else "Bilinmiyor"

    # En çok gidilen ülkeyi bul
    most_visited_country_mode = data["country"].mode()
    most_visited_country = most_visited_country_mode[0] if not most_visited_country_mode.empty else "Bilinmiyor"

    # En düşük ve en yüksek puanı bul
    lowest_score_given = data["review_score"].min(skipna=True)
    highest_score_given = data["review_score"].max(skipna=True)

    # En çok gidilen yeri bul (Eğer boşsa "Bilinmiyor" ata)
    most_visited_place_mode = data["hotel_name"].mode()
    most_visited_place = most_visited_place_mode[0] if not most_visited_place_mode.empty else "Bilinmiyor"

    # Farklı otel sayısını bul
    number_of_different_hotels = data["hotel_name"].nunique()

    # Duygu dağılımı
    comment_sentiment_distribution = data["Yorum Duygusu"].value_counts().to_dict()

    # Genel duygu analizi
    general_sentiment_analysis = data["Yorum Duygusu"].mode()[0] if not data["Yorum Duygusu"].empty else "Bilinmiyor"

    user_data.append([user, total_reviews, avg_user_rating, most_visited_place, avg_user_rating,
                      number_of_different_hotels, most_visited_country, lowest_score_given,
                      highest_score_given, comment_sentiment_distribution, general_sentiment_analysis])

# Yeni DataFrame oluştur
user_columns = ["UserID", "comments", "average_score_given", "most_visited_place",
                "average_score_of_places_visited", "number_of_different_hotel",
                "most_visited_country", "lowest_score_given", "highest_score_given",
                "comment_sentiment_distribution", "general_sentiment_analysis"]

user_analysis_df = pd.DataFrame(user_data, columns=user_columns)

# Yeni Excel dosyasına kaydet
user_analysis_df.to_excel(output_user_file_path, index=False, engine="openpyxl")

print(f"Kullanıcı analizi tamamlandı! Sonuçlar '{output_user_file_path}' dosyasına kaydedildi.")
