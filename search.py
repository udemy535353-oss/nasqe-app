import os
from bs4 import BeautifulSoup
import json

def create_inverted_index(data_folder):
    """
    Veri klasöründeki HTML dosyalarını okur ve bir ters indeks oluşturur.
    """
    inverted_index = {}
    stop_words = {"bir", "ve", "ile", "ama", "için", "bu", "şu", "o"} # Basit anlamsız kelimeler

    for filename in os.listdir(data_folder):
        if filename.endswith('.html'):
            filepath = os.path.join(data_folder, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

                # Sadece görünür metni al, script ve style etiketlerini yok say
                for script_or_style in soup(["script", "style"]):
                    script_or_style.decompose()
                
                text = soup.get_text()
                words = text.lower().split() # Kelimelere ayır ve küçük harfe çevir

                for word in words:
                    # Noktalama işaretlerini temizle
                    word = ''.join(filter(str.isalnum, word))
                    
                    if word and word not in stop_words:
                        if word not in inverted_index:
                            inverted_index[word] = []
                        if filename not in inverted_index[word]:
                            inverted_index[word].append(filename)
    
    # İndeksi JSON dosyasına yaz
    with open('index.json', 'w', encoding='utf-8') as f:
        json.dump(inverted_index, f, ensure_ascii=False, indent=4)
    
    print("İndeks oluşturuldu ve 'index.json' dosyasına kaydedildi.")

# --- Indexer'ı Başlat ---
if __name__ == "__main__":
    create_inverted_index('data')