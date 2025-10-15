import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin, urlparse

# Gezilen verileri kaydetmek için bir klasör oluşturalım
if not os.path.exists('data'):
    os.makedirs('data')

def is_valid(url):
    """Sadece geçerli URL'leri kontrol eder (örn: mailto:, javascript: linklerini engeller)"""
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def crawl(start_url, max_pages=10):
    """
    Belirtilen URL'den başlayarak web sayfalarını gezer ve kaydeder.
    """
    # Ziyaret edilecek URL'ler için bir liste (kuyruk gibi davranacak)
    urls_to_visit = [start_url]
    # Daha önce ziyaret edilen URL'leri takip etmek için bir set (hızlı kontrol için)
    visited_urls = set()
    page_count = 0

    while urls_to_visit and page_count < max_pages:
        url = urls_to_visit.pop(0)
        if url in visited_urls:
            continue

        print(f"Geziliyor: {url}")
        try:
            response = requests.get(url, timeout=5)
            # Bir siteye sürekli istek atmamak için biraz bekle
            time.sleep(1) 
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                visited_urls.add(url)
                
                # Sayfa içeriğini kaydet
                filename = os.path.join('data', f"page_{page_count}.html")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(soup.prettify()) # prettify() ile daha okunaklı HTML
                
                page_count += 1

                # Sayfadaki tüm linkleri bul ve sıraya ekle
                for link in soup.find_all('a', href=True):
                    # Linki tam bir URL'ye dönüştür (örn: /about -> http://site.com/about)
                    absolute_link = urljoin(url, link['href'])
                    if is_valid(absolute_link) and absolute_link not in visited_urls:
                        urls_to_visit.append(absolute_link)

        except requests.RequestException as e:
            print(f"Hata: {url} adresine ulaşılamadı. {e}")

# --- Crawler'ı Başlat ---
if __name__ == "__main__":
    # Wikipedia'nın teknoloji portalından başlayalım
    # DİKKAT: Çok büyük siteleri gezmek uzun sürer ve bant genişliği harcar.
    # Küçük ve kontrollü bir site ile başlamak en iyisidir.
    crawl("https://tr.wikipedia.org/wiki/Teknoloji", max_pages=20)
    print(f"\nTarama tamamlandı. 'data' klasörüne {len(os.listdir('data'))} sayfa kaydedildi.")