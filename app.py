# server.py
import socket
import threading

# --- Ayarlar ---
HOST = '0.0.0.0'  # Tüm ağ arayüzlerinden gelen bağlantıları dinle
PORT = 65432       # Kullanılmayan bir port numarası
MAX_CLIENTS = 2    # Sadece iki istemciye izin verilecek

# --- Global Değişkenler ---
clients = [] # Bağlı istemcilerin soketlerini tutacak liste
client_threads = [] # İstemci thread'lerini tutacak liste
lock = threading.Lock() # Paylaşılan kaynaklara erişimi senkronize etmek için kilit

# --- Yardımcı Fonksiyonlar ---
def broadcast_message(message, sender_socket=None):
    """
    Mesajı gönderen hariç tüm bağlı istemcilere gönderir.
    Eğer sender_socket None ise, tüm istemcilere gönderir (sunucu mesajları için).
    """
    with lock: # Birden fazla thread'in aynı anda clients listesini değiştirmesini engelle
        for client_socket in clients:
            if client_socket != sender_socket:
                try:
                    client_socket.sendall(message.encode('utf-8'))
                except socket.error:
                    # İstemciye mesaj gönderilemezse, bağlantıyı kes ve listeden çıkar
                    print(f"İstemciye mesaj gönderilemedi: {client_socket.getpeername()}")
                    remove_client(client_socket)

def remove_client(client_socket):
    """Bağlantısı kesilen istemciyi listeden kaldırır."""
    if client_socket in clients:
        clients.remove(client_socket)
        print(f"İstemci ayrıldı: {client_socket.getpeername()}. Kalan istemciler: {len(clients)}")
        # Eğer bir istemci ayrılırsa ve diğer istemci hala bağlıysa ona bilgi ver
        if len(clients) == 1:
            try:
                clients[0].sendall("Diğer kullanıcı sohbetten ayrıldı.".encode('utf-8'))
            except:
                pass # Diğer istemci de zaten ayrılmış olabilir

def handle_client(client_socket, client_address):
    """Her bir istemci bağlantısını ayrı bir thread'de yönetir."""
    print(f"[YENİ BAĞLANTI] {client_address} bağlandı.")
    
    # İstemci listesine ekle
    with lock:
        clients.append(client_socket)

    # Diğer istemciye yeni bir kullanıcının katıldığını bildir (eğer varsa)
    if len(clients) == MAX_CLIENTS:
        broadcast_message(f"[SİSTEM] Diğer kullanıcı sohbete katıldı. Mesajlaşmaya başlayabilirsiniz!", client_socket)
        # Kendisine de bildirim gönder
        client_socket.sendall(f"[SİSTEM] Sohbete katıldınız. Diğer kullanıcı bekleniyor... (Eğer zaten bağlıysa mesajlaşabilirsiniz)".encode('utf-8'))

    elif len(clients) < MAX_CLIENTS:
         client_socket.sendall(f"[SİSTEM] Sohbete katıldınız. Diğer kullanıcının bağlanması bekleniyor...".encode('utf-8'))


    try:
        while True:
            # İstemciden mesaj al
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                # Boş mesaj, istemcinin bağlantıyı kapattığı anlamına gelir
                print(f"[BAĞLANTI KESİLDİ] {client_address} bağlantıyı kapattı.")
                break
            
            print(f"[{client_address}] {message}")
            
            # Mesajı diğer istemciye ilet
            # Sadece iki istemci olduğu için, gönderen hariç diğerine gönder
            if len(clients) == MAX_CLIENTS: # Sadece iki kişi varsa mesajı ilet
                broadcast_message(f"[{client_address[1]}] {message}", client_socket)
            else:
                client_socket.sendall("[SİSTEM] Henüz diğer kullanıcı bağlanmadı. Lütfen bekleyin.".encode('utf-8'))

    except ConnectionResetError:
        print(f"[BAĞLANTI SIFIRLANDI] {client_address} bağlantıyı aniden kapattı.")
    except Exception as e:
        print(f"[HATA] {client_address} ile iletişimde hata: {e}")
    finally:
        # İstemci bağlantısı kesildiğinde yapılacak temizlik
        with lock:
            remove_client(client_socket)
        client_socket.close()

def start_server():
    """Sunucuyu başlatır ve gelen bağlantıları dinler."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SO_REUSEADDR seçeneği, sunucunun aynı adresi hemen yeniden kullanabilmesini sağlar
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
    except socket.error as e:
        print(f"Sunucu başlatılamadı: {e}")
        return

    server_socket.listen(MAX_CLIENTS) # En fazla MAX_CLIENTS kadar bağlantıyı beklemeye al
    print(f"[DİNLENİYOR] Sunucu {HOST}:{PORT} adresinde dinlemede...")

    try:
        while True:
            if len(clients) < MAX_CLIENTS:
                try:
                    # Yeni bir bağlantı kabul et
                    client_socket, client_address = server_socket.accept()
                except socket.error: # Sunucu soketi kapatıldığında döngüden çık
                    print("[KAPATILIYOR] Sunucu soketi kapatıldı.")
                    break
                
                # Her istemci için yeni bir thread başlat
                thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                thread.daemon = True # Ana program bittiğinde thread'lerin de bitmesini sağlar
                thread.start()
                client_threads.append(thread)
            else:
                # Maksimum istemci sayısına ulaşıldı, yeni bağlantıları reddetmek yerine bekleyebiliriz
                # veya geçici olarak reddedebiliriz. Bu basit örnekte, accept() bloke olacağı için
                # yeni bağlantı kabul etmeyecek. Daha gelişmiş bir sistemde reddetme mantığı eklenebilir.
                pass # Şimdilik bir şey yapma, accept() zaten yeni bağlantı almayacak
                
    except KeyboardInterrupt:
        print("[KAPATILIYOR] Sunucu kapatılıyor...")
    finally:
        print("Tüm istemci bağlantıları kapatılıyor...")
        with lock:
            for client_socket in clients:
                try:
                    client_socket.sendall("[SİSTEM] Sunucu kapatılıyor. Bağlantınız kesilecek.".encode('utf-8'))
                    client_socket.close()
                except socket.error:
                    pass # İstemci zaten kapanmış olabilir
            clients.clear()

        for thread in client_threads:
            if thread.is_alive():
                # Thread'leri doğrudan sonlandırmak iyi bir pratik değildir,
                # ancak bu basit örnek için kabul edilebilir.
                # Daha iyi bir yöntem, thread'lere bir sonlandırma sinyali göndermek olurdu.
                pass
        
        server_socket.close()
        print("Sunucu başarıyla kapatıldı.")

if __name__ == "__main__":
    start_server()
