import sqlite3
import sys
import os
import time
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
l = list()
alıcı = "rot"
class pencere(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.bağlantı()
        self.init_ui()
    def bağlantı(self):
        self.con = sqlite3.connect("mys.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS giriş(kullanıcı TEXT, şifre TEXT)")
        self.con.commit()



    def init_ui(self):
        self.ad = QtWidgets.QLineEdit()
        self.ad.setStyleSheet("""
                                background-color: #ffffff;
                              
                              
                              
                              
                              """)
        self.ad.setObjectName("messageLabel")
        self.ad.setPlaceholderText("kullanıcı adınızı girin")
        self.sıfırla = QtWidgets.QPushButton("Sıfırla")
        self.sıfırla.setObjectName("reset")
        self.sıfırla.setStyleSheet("""
                                   QPushButton { /* Tüm butonlar için genel stil */
            background-color: #65b5b8; /* Mavi */
        }
            
        }
        QPushButton:hover {
            background-color: #609a9c; /* Hover rengi */
        }
        QPushButton:pressed {
            background-color: #426f70; /* Basılma rengi */
                                   
                                   
                                    """)
        self.parola = QtWidgets.QLineEdit()
        self.parola.setPlaceholderText("parola girin")
        self.parola.setStyleSheet("""
                                    background-color: #ffffff;
                                  
                                  
                                  
                                  
                                  """)
        self.parola.setEchoMode(QtWidgets.QLineEdit.Password)
        self.yazı = QtWidgets.QLabel("")
        self.yazı.setWordWrap(True)
        self.yazı.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.yazı.setFixedSize(650,100)
        self.yazı.setStyleSheet("""
                                QLabel {
                                    background-color:#529c80;
                                    font-size: 16px;
                                    font-family: "Inter";
                                    padding: 8px;
                                    border: 3px solid #ffffff;
                                    border-radius: 10px;
                                }
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                """)
        self.enter_click = QtWidgets.QPushButton("Giriş")
        self.enter_click.setObjectName("enter")
        self.enter_click.setStyleSheet("""
                                   QPushButton { 
            background-color: #bcc24e; /* Mavi */
        }
            
        }
        QPushButton:hover {
            background-color: #9a9e49; 
        }
        QPushButton:pressed {
            background-color: #6b6e32; 
        
                                   
                                   
                                    """)
        self.kaydol = QtWidgets.QPushButton("Kayıt")
        self.kaydol.setObjectName("kayit")
        self.kaydol.setStyleSheet("""
                                   QPushButton { 
            background-color: #d44b28; /* Mavi */
        }
            
        }
        QPushButton:hover {
            background-color: #ab4d35; 
        }
        QPushButton:pressed {
            background-color: #70301f; 
        
                                   
                                   
                                    """)
        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.ad)
        v_box.addWidget(self.parola)
        v_box.addWidget(self.yazı)
        v_box.addWidget(self.enter_click)
        v_box.addWidget(self.kaydol)
        v_box.addWidget(self.sıfırla)
        v_box.addStretch()
        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()
        self.setLayout(h_box)
        self.setWindowTitle("Giriş")
        self.enter_click.clicked.connect(self.enter)
        self.kaydol.clicked.connect(self.sign)
        self.sıfırla.clicked.connect(self.reset)
        self.show()

    def enter(self):
        kullanıcıb = self.ad.text()
        şifrer = self.parola.text()
        self.cursor.execute("SELECT * FROM giriş WHERE kullanıcı = ? AND şifre = ?",((kullanıcıb,şifrer)))
        data = self.cursor.fetchall()
        if kullanıcıb == "" or şifrer == "":
            self.yazı.setText("boş alanları doldur")
        elif len(data) == 0:
            self.yazı.setText("böyle böyle bir kullanıcı yok")
        else:
            self.yazı.setText("giriş başarılı")
            self.ad.clear()
            self.parola.clear()
    def sign(self):
        kullanıcı = self.ad.text()
        şifre = self.parola.text()
        self.cursor.execute("SELECT kullanıcı FROM giriş WHERE kullanıcı = ?", (kullanıcı,))
        moe = self.cursor.fetchall()
        if kullanıcı == "" or şifre == "":
            self.yazı.setText("boş alanları doldur")
        if len(kullanıcı) < 8 or len(şifre) < 8:
            self.yazı.setText("bu kadar kısa olamaz")
            return
        if len(moe) > 0:
            self.yazı.setText("Bu kullanıcı adı zaten alınmış.")
            return
            
        else:
            self.yazı.setText("kayıt yapılıyor...")
            self.yazı.setText("kayıt başarılı")
            self.ad.clear()
            self.parola.clear()
            self.cursor.execute("Insert into giriş Values(?,?)",(kullanıcı,şifre))
            self.con.commit()
    def reset(self):
        kullanici_adi = self.ad.text()
        yeni_sifre = self.parola.text()
        self.cursor.execute("select kullanıcı from giriş")
        moe = self.cursor.fetchall()
        if kullanici_adi == "" or yeni_sifre == "":
            self.yazı.setText("boş alanları doldur")
        self.cursor.execute("select * from giriş where kullanıcı = ?",(kullanici_adi,))
        data = self.cursor.fetchall()
        if len(data) == 0:
                self.yazı.setText("böyle bir kullanıcı yok")
        
        else:
            self.yazı.setText("sıfırlanıyor...")
            time.sleep(2)
            self.yazı.setText("sıfırlama başarılı")
            self.ad.clear()
            self.parola.clear()
            self.cursor.execute("update giriş set şifre  = ? where kullanıcı = ?",(yeni_sifre, kullanici_adi))
            self.con.commit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
                      background-color:#a66fad;
                      }
        QLineEdit {
                      background-color: #ffffff;
                      color: #333333; /* Siyahımsı metin rengi */
                      font-size: 16px;
                      font-weight: bold;
                      padding: 8px;
                      border: 1px solid #cccccc;
                      border-radius: 10px;
                      }
        QPushButton {
                      color: #000000;
                      font-size: 10px;
                      font-weight: bold;
                      padding: 8px;
                      border: 3px solid #ffffff;
                      border-radius: 15px;
                      }
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      """)
    pencere=pencere()
    sys.exit(app.exec_())


        