from PyQt5.QtWidgets import QMainWindow,QLabel, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
import string
import random
import sys
from datetime import datetime
import sqlite3

import os
from datetime import date

# Programın çalıştığı klasörün yolunu al
# os.getcwd() da kullanılabilir ama bu daha kesin bir yöntemdir
# Eğer bir .exe'ye dönüştürülürse de çalışır
# Kaydedilecek dosyanın tam yolu
program_folder = os.path.dirname(os.path.abspath(__file__))
start_date_file = os.path.join(program_folder, "start_date.txt")

class mobile(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.main()
        self.create()
    def create(self):
        self.con = sqlite3.connect("keys.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS keys(key TEXT)")
        self.con.commit()
        



    def set_start_date():
        """
    Programın başlangıç tarihini, programın çalıştığı klasördeki
    bir dosyaya kaydeder.
    """
        if not os.path.exists(start_date_file):
            with open(start_date_file, "w") as f:
                f.write(date.today().isoformat())
            print("Başlangıç tarihi kaydedildi.")
        else:
            print("Başlangıç tarihi dosyası zaten mevcut.")

    def calculate_remaining_days(self):
        """
        Kaydedilmiş tarihi okur ve kalan gün sayısını hesaplar.
        """
        try:
            with open(start_date_file, "r") as f:
                start_date_str = f.read()
                start_date = date.fromisoformat(start_date_str)
            
                today = date.today()
                delta = today - start_date
            
                self.remaining_days = 30 - delta.days
                return remaining_days
        except FileNotFoundError:
        # Dosya bulunamazsa, ilk çalıştırma olarak kabul et
            
            return 30
        except Exception as e:
            print(f"Hata: {e}")
        return -1
    def main(self):
        self.text = QLabel("30 day remainig")
        self.input = QLineEdit(placeholderText="Key")
        self.button = QPushButton("Unlock")
        self.button.setStyleSheet("margin-bottom: 250px;")
        self.input.setFixedSize(200, 30)
        time = datetime.now()
        print(time)
        v = QVBoxLayout()
        h = QHBoxLayout()
        v.addWidget(self.text)
        v.addWidget(self.input)
        v.addWidget(self.button)
        
        h.addStretch(1)
        h.addLayout(v)
        
        h.addStretch(1)
        self.setLayout(h)
        self.setWindowTitle("Key Unlocker")
        self.button.clicked.connect(self.check)
        self.show()
    def check(self):
        st = self.calculate_remaining_days()
        key = self.input.text()
        self.cursor.execute("select key from keys where key = ?",(key,))
        data = self.cursor.fetchall()
        if len(data) == 0:
            remaining_days = self.calculate_remaining_days()
            if remaining_days > 0:
            
                self.text.setText("{} days remaining".format(st))
            elif remaining_days == 0:
                self.text.setText("Last day! Please enter a valid key. {}".format(st))
            else:
                self.text.setText("Trial period expired. Please enter a valid key.")
            self.input.clear()
        else:
            self.text.setText("Program unlocked successfully!")
            self.input.clear()
app = QApplication(sys.argv)
window = mobile()

sys.exit(app.exec_())
