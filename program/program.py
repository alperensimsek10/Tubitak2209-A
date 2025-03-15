from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
import random
import os
import logging
from openpyxl import load_workbook
import re

# Log dosyası ayarı
logging.basicConfig(filename='hatalar.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

# Rastgele bekleme süresi
def rastgele_bekle(min_saniye=2, max_saniye=5):
    sleep(random.uniform(min_saniye, max_saniye))

# Fare hareketlerini simüle etme
def fare_hareketi_simule_et(driver):
    action = ActionChains(driver)
    try:
        for _ in range(random.randint(5, 10)):
            x_offset = random.randint(-50, 50)
            y_offset = random.randint(-50, 50)
            action.move_by_offset(x_offset, y_offset).perform()
            rastgele_bekle(0.2, 0.8)
    except Exception as e:
        logging.error(f"Fare hareketi simülasyonunda hata: {e}")
        action.reset_actions()

# İnsansı tıklama işlemi
def insansi_tiklama(driver, element):
    action = ActionChains(driver)
    try:
        action.move_to_element(element)
        rastgele_bekle(1, 2)
        action.click(element).perform()
    except Exception as e:
        logging.error(f"İnsansı tıklama hatası: {e}")

# Çerez onayı işlemi
def cerez_onayi(driver):
    try:
        accept_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "accept")]'))
        )
        insansi_tiklama(driver, accept_button)
    except Exception as e:
        logging.warning(f"Çerez onayı butonu bulunamadı veya hata oluştu: {e}")

# İşlenmiş kullanıcıları yükleme
def kaydedilen_konuklari_yukle(dosya_yolu):
    if os.path.exists(dosya_yolu):
        with open(dosya_yolu, 'r') as dosya:
            return set(dosya.read().splitlines())
    return set()

# İşlenen kullanıcıyı kaydetme
def islenen_konugu_kaydet(dosya_yolu, kullanici_adi):
    with open(dosya_yolu, 'a') as dosya:
        dosya.write(f"{kullanici_adi}\n")
# Kullanıcı bilgilerini işleme fonksiyonu
def kullanici_bilgilerini_isle(driver, kullanici_adi):
    profil_url = f"https://www.tripadvisor.com/Profile/{kullanici_adi.strip()}"
    driver.get(profil_url)
    rastgele_bekle()

    if "This user doesn’t exist" in driver.page_source:
        logging.warning(f"Kullanıcı bulunamadı: {kullanici_adi}")
        return None

    cerez_onayi(driver)
    fare_hareketi_simule_et(driver)

    entry = {
        "Kullanıcı Adı": kullanici_adi,
        "Katkı Sayısı": '0',
        "Takipçi Sayısı": '0',
        "Takip Ettikleri": '0',
        "Konum": 'veri bulunamadı',
        "Katılma Tarihi": 'veri bulunamadı',
        "Yorum Tarihi": 'veri bulunamadı',
        "Yorum Puanı": 0.0,
        "Mekan Adı": 'veri bulunamadı',
        "Mekan Puanı": 0.0,
        "Yorum Başlığı": 'veri bulunamadı',
        "Yorum Metni": 'veri bulunamadı',
    }

    try:
        entry['Katkı Sayısı'] = driver.find_element(By.CSS_SELECTOR,
                                                    'span[class="rNZKv"]:nth-of-type(2) > a[class="etCOn b Wc _S"]').text or "0"
    except Exception as e:
        logging.warning(f"Katkı Sayısı bilgisi alınamadı ({kullanici_adi}): {e}")

    try:
        entry['Takipçi Sayısı'] = driver.find_element(By.CSS_SELECTOR,
                                                      'span[class="rNZKv"]:nth-of-type(3) > a[class="etCOn b Wc _S"]').text or "0"
    except Exception as e:
        logging.warning(f"Takipçi Sayısı bilgisi alınamadı ({kullanici_adi}): {e}")

    try:
        entry['Takip Ettikleri'] = driver.find_element(By.CSS_SELECTOR,
                                                       'span[class="rNZKv"]:nth-of-type(1) > a[class="etCOn b Wc _S"]').text or "0"
    except Exception as e:
        logging.warning(f"Takip Ettikleri bilgisi alınamadı ({kullanici_adi}): {e}")

    try:
        entry['Konum'] = driver.find_element(By.CSS_SELECTOR, 'span[class="PacFI _R S4 H3 LXUOn default"]').text
    except Exception as e:
        logging.warning(f"Konum bilgisi alınamadı ({kullanici_adi}): {e}")

    try:
        entry['Katılma Tarihi'] = driver.find_element(By.CSS_SELECTOR, 'span.ECVao._R.H3').text
    except Exception as e:
        logging.warning(f"Katılma Tarihi alınamadı ({kullanici_adi}): {e}")

    yorumlar = driver.find_elements(By.CSS_SELECTOR, 'div[class="JnUAZ"]')
    if not yorumlar:
        logging.warning(f"Yorum bulunamadı ({kullanici_adi})")
        return None

    tum_yorumlar = []
    for yorum_div in yorumlar:
        yorum_entry = entry.copy()

        try:
            yorum_tarihi_element = yorum_div.find_element(By.CSS_SELECTOR, 'div.LmTJN.S4.H3.Ci > span')
            yorum_entry['Yorum Tarihi'] = yorum_tarihi_element.text.split(":")[-1].strip()
        except:
            yorum_entry['Yorum Tarihi'] = None

        try:
            yorum_puani_element = yorum_div.find_element(By.CSS_SELECTOR, "div.muQub.VrCoN svg title")
            yorum_puani_text = yorum_puani_element.get_attribute("textContent")
            yorum_puani = re.search(r"(\d+\.\d+)", yorum_puani_text)
            yorum_entry['Yorum Puanı'] = float(yorum_puani.group(1)) if yorum_puani else 0.0
        except:
            yorum_entry['Yorum Puanı'] = 0.0

        try:
            yorum_entry['Mekan Adı'] = yorum_div.find_element(By.CSS_SELECTOR, "div.Jkczm.ui_link").text
        except:
            yorum_entry['Mekan Adı'] = None

        try:
            mekan_puani_element = yorum_div.find_element(By.CSS_SELECTOR, "div.jVDab.W.f.u.w.GOdjs")
            mekan_puani_text = mekan_puani_element.get_attribute("aria-label")
            mekan_puani = re.search(r"(\d+\.\d+)", mekan_puani_text)
            yorum_entry['Mekan Puanı'] = float(mekan_puani.group(1)) if mekan_puani else 0.0
        except:
            yorum_entry['Mekan Puanı'] = 0.0

        try:
            yorum_entry['Yorum Başlığı'] = yorum_div.find_element(By.CSS_SELECTOR, 'div[class="AzIrY b _a VrCoN"]').text
        except:
            yorum_entry['Yorum Başlığı'] = None

        try:
            yorum_entry['Yorum Metni'] = yorum_div.find_element(By.CSS_SELECTOR,
                                                                'div[class="bdHFy _a"] q[class="BTPVX"]').text
        except:
            yorum_entry['Yorum Metni'] = None

        tum_yorumlar.append(yorum_entry)

    return tum_yorumlar


# Veriyi Excel dosyasına ekleme
def excel_dosyasina_ekle(dosya_yolu, veri):
    try:
        if os.path.exists(dosya_yolu):
            wb = load_workbook(dosya_yolu)
            sheet = wb.active
            sheet.append(list(veri.values()))
            wb.save(dosya_yolu)
        else:
            df = pd.DataFrame([veri])
            df.to_excel(dosya_yolu, index=False)
    except Exception as e:
        logging.error(f"Veri Excel dosyasına kaydedilemedi: {e}")

# Dosya yolları
excel_dosyasi = r"C:\\Projects\\TripAdvisor\\TripAdvisor-master\\users\\konuk_idleri.xlsx"
islenen_dosya = r"C:\\Projects\\TripAdvisor\\TripAdvisor-master\\users\\islenen_konuklar.txt"
output_dosyasi = r"C:\\Projects\\TripAdvisor\\TripAdvisor-master\\users\\KonukOtel.xlsx"

if not os.path.exists(excel_dosyasi):
    logging.error(f"Excel dosyası bulunamadı: {excel_dosyasi}")
    exit()

# İşlenmiş kullanıcıları yükle
islenen_konuklar = kaydedilen_konuklari_yukle(islenen_dosya)

# Kullanıcı verilerini yükle
try:
    kullanici_verileri = pd.read_excel(excel_dosyasi, engine='openpyxl')
    kullanici_verileri.columns = kullanici_verileri.columns.str.strip()
    if 'kullanici_adi' not in kullanici_verileri.columns:
        logging.error("Excel dosyasında 'kullanici_adi' sütunu bulunamadı.")
        exit()
    kullanici_adlari = [k for k in kullanici_verileri['kullanici_adi'].dropna().tolist() if k not in islenen_konuklar]
    random.shuffle(kullanici_adlari)
except Exception as e:
    logging.error(f"Excel dosyası okunurken hata oluştu: {e}")
    exit()

# Selenium seçenekleri"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

while True:
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script(""" 
        delete navigator.__proto__.webdriver; 
        Object.defineProperty(navigator, 'webdriver', { get: () => false }); 
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); 
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] }); 
        window.navigator.chrome = {runtime: {}}; 
    """)

    for kullanici_adi in kullanici_adlari:
        deneme_sayisi = 0
        basarili = False

        while deneme_sayisi < 2 and not basarili:
            try:
                yorumlar = kullanici_bilgilerini_isle(driver, kullanici_adi)
                if yorumlar:
                    for yorum in yorumlar:  # Tüm yorumları tek tek kaydet
                        excel_dosyasina_ekle(output_dosyasi, yorum)
                    islenen_konugu_kaydet(islenen_dosya, kullanici_adi)
                    basarili = True
            except Exception as e:
                deneme_sayisi += 1
                logging.error(f"Bir hata oluştu ({kullanici_adi}): {e}. {deneme_sayisi}. deneme")
                rastgele_bekle(300, 600)

        if not basarili:
            logging.error(f"{kullanici_adi} 2 denemeden sonra işlenemedi.")

        rastgele_bekle(180, 600)