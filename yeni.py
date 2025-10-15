import sys
import sqlite3
import string
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox, QGridLayout
)
from PyQt5.QtCore import Qt # Qt.AlignRight gibi hizalamalar için

class MobileApp(QWidget): # Sınıf adını MobileApp olarak değiştirdim
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telefon Numarası Yönetimi") # Pencere başlığını güncelledim
        self.setFixedSize(300, 400)
        self.connect_db() # Türkçe metot adlarını İngilizce yaptım
        self.init_ui()

    def connect_db(self):
        """Veritabanı bağlantısını kurar ve tabloyu oluşturur."""
        try:
            self.con = sqlite3.connect("phone_numbers.db") # Veritabanı adını değiştirdim
            self.cursor = self.con.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS numbers (number TEXT UNIQUE)") # Tablo adı ve sütun adını güncelledim, UNIQUE ekledim
            self.con.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Veritabanına bağlanırken hata oluştu: {e}")
            sys.exit(1) # Hata durumunda uygulamayı kapat

    def generate_random_number(self, length=11):
        """Belirtilen uzunlukta rastgele bir sayı dizisi oluşturur."""
        characters = string.digits
        code = "".join(random.choice(characters) for _ in range(length))
        return code

    def init_ui(self):
        """Kullanıcı arayüzünü başlatır ve elemanları yerleştirir."""
        # Ana Dikey Düzen (Main Vertical Layout)
        main_layout = QVBoxLayout()

        # 1. Sorgu ve Mesaj Alanları (Üst Kısım)
        input_layout = QHBoxLayout() # Yatay düzen
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Numara veya başlangıç girin")
        self.query_input.setFixedSize(180, 35) # Boyutunu sabitledim
        self.query_input.setObjectName("queryInput") # CSS için ObjectName belirttim
        
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.message_label.setWordWrap(True) # Uzun metinlerde satır atlamasını sağlar
        self.message_label.setObjectName("messageLabel") # CSS için ObjectName belirttim

        input_layout.addWidget(self.query_input)
        input_layout.addStretch(1) # QLineEdit'in sağında boşluk bırakır
        
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.message_label) # Mesaj label'ı ayrı bir satırda

        # 2. Butonlar (Alt Kısım)
        button_grid_layout = QGridLayout() # Butonları düzenli yerleştirmek için ızgara düzeni kullanıyorum
        
        self.check_button = QPushButton("Numara Sorgula")
        self.check_button.setObjectName("checkButton")
        
        self.generate_button = QPushButton("Numara Üret ve Kaydet")
        self.generate_button.setObjectName("generateButton")
        
        self.view_button = QPushButton("Numaraları Görüntüle")
        self.view_button.setObjectName("viewButton")

        # Butonları ızgara düzenine ekle
        button_grid_layout.addWidget(self.check_button, 0, 0) # Satır 0, Sütun 0
        button_grid_layout.addWidget(self.generate_button, 0, 1) # Satır 0, Sütun 1
        button_grid_layout.addWidget(self.view_button, 1, 0, 1, 2) # Satır 1, Sütun 0'dan başlayıp 2 sütunu kapla

        main_layout.addLayout(button_grid_layout)
        main_layout.addStretch(1) # Butonların altına boşluk bırakır

        self.setLayout(main_layout)

        # Sinyal ve Slot Bağlantıları
        self.generate_button.clicked.connect(self.handle_generate_and_save) # Metot adlarını güncelledim
        self.check_button.clicked.connect(self.handle_check_number)
        self.view_button.clicked.connect(self.handle_view_numbers)

        self.message_label.setText("Uygulamaya hoş geldiniz!") # Başlangıç mesajı

    def handle_generate_and_save(self):
        """Rastgele numara üretir ve veritabanına kaydeder."""
        max_attempts = 10000 # Maksimum deneme sayısı
        attempts = 0
        while attempts < max_attempts:
            new_number = self.generate_random_number()
            if new_number.startswith("05"):
                try:
                    self.cursor.execute("SELECT number FROM numbers WHERE number = ?", (new_number,))
                    data = self.cursor.fetchone()
                    if data is None: # Numara veritabanında yoksa
                        self.cursor.execute("INSERT INTO numbers VALUES (?)", (new_number,))
                        self.con.commit()
                        self.message_label.setText(f"Numara başarıyla eklendi: {new_number}")
                        return # Başarılı olduysa döngüden çık
                    else:
                        attempts += 1 # Numara zaten varsa tekrar dene
                except sqlite3.Error as e:
                    self.message_label.setText(f"Veritabanı hatası: {e}")
                    QMessageBox.warning(self, "Veritabanı Hatası", f"Numara kaydederken hata: {e}")
                    return
            else:
                attempts += 1 # 05 ile başlamıyorsa tekrar dene
        
        self.message_label.setText(f"Belirtilen koşullarda {max_attempts} denemede numara bulunamadı.")


    def handle_check_number(self):
        """Girilen numaranın veritabanında olup olmadığını kontrol eder."""
        number_to_check = self.query_input.text().strip()
        if not number_to_check:
            self.message_label.setText("Lütfen sorgulamak için bir numara girin.")
            return

        try:
            self.cursor.execute("SELECT number FROM numbers WHERE number = ?", (number_to_check,))
            data = self.cursor.fetchone()
            if data is None:
                self.message_label.setText(f"'{number_to_check}' numarası veritabanında yok.")
            else:
                self.message_label.setText(f"'{number_to_check}' numarası bulundu.")
        except sqlite3.Error as e:
            self.message_label.setText(f"Veritabanı hatası: {e}")
            QMessageBox.warning(self, "Veritabanı Hatası", f"Numara sorgularken hata: {e}")

    def handle_view_numbers(self):
        """Veritabanındaki numaraları görüntüler veya başlangıca göre filtreler."""
        search_prefix = self.query_input.text().strip()
        
        try:
            if search_prefix:
                self.cursor.execute("SELECT number FROM numbers WHERE number LIKE ?", (search_prefix + '%',))
            else:
                self.cursor.execute("SELECT number FROM numbers")
            
            found_numbers = [row[0] for row in self.cursor.fetchall()]

            if found_numbers:
                display_text = "Bulunan Numaralar:\n" + "\n".join(found_numbers)
                self.message_label.setText(display_text)
            else:
                self.message_label.setText("Numara bulunamadı.")
        except sqlite3.Error as e:
            self.message_label.setText(f"Veritabanı hatası: {e}")
            QMessageBox.warning(self, "Veritabanı Hatası", f"Numaraları görüntülerken hata: {e}")

    def closeEvent(self, event):
        """Uygulama kapatılırken veritabanı bağlantısını kapatır."""
        if self.con:
            self.con.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: #f0f0f0; /* Açık gri arkaplan */
            font-family: "Segoe UI", "Helvetica Neue", sans-serif; /* Daha modern font */
        }
        #queryInput { /* QLineEdit için stil */
            background-color: #ffffff;
            color: #333333; /* Siyahımsı metin rengi */
            font-size: 16px;
            padding: 8px;
            border: 1px solid #cccccc;
            border-radius: 5px;
        }
        #messageLabel { /* QLabel için stil */
            color: #2e5375; /* Mavi tonu */
            font-size: 15px;
            font-weight: bold;
            padding: 5px;
            min-height: 80px; /* Mesajların sığması için min yükseklik */
            background-color: #e9e9e9;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-top: 10px; /* Üstte boşluk */
        }
        QPushButton { /* Tüm butonlar için genel stil */
            background-color: #007bff; /* Mavi */
            color: white;
            font-size: 14px;
            font-weight: bold;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            margin: 5px; /* Butonlar arasında boşluk */
        }
        QPushButton:hover {
            background-color: #0056b3; /* Hover rengi */
        }
        QPushButton:pressed {
            background-color: #004085; /* Basılma rengi */
        }
        #generateButton { /* "Launch" butonu için özel stil (yeşil) */
            background-color: #28a745;
        }
        #generateButton:hover {
            background-color: #218838;
        }
        #generateButton:pressed {
            background-color: #1e7e34;
        }
        #viewButton { /* "View" butonu için özel stil (mor) */
            background-color: #6f42c1;
        }
        #viewButton:hover {
            background-color: #563d7c;
        }
        #viewButton:pressed {
            background-color: #492e66;
        }
    """)
    window = MobileApp()
    window.show()
    sys.exit(app.exec_())