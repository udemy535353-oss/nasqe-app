from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import os
class pencere(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.temizle = QtWidgets.QPushButton("Temizle")
        self.ac = QtWidgets.QPushButton("Aç")
        self.kaydet = QtWidgets.QPushButton("Kaydet")
        self.yazi = QtWidgets.QTextEdit()
        v = QtWidgets.QVBoxLayout()
        v.addWidget(self.temizle)
        v.addWidget(self.ac)
        v.addWidget(self.kaydet)
        h = QtWidgets.QHBoxLayout()
        h.addWidget(self.yazi)
        h.addLayout(v)
        self.setLayout(h)
        self.setWindowTitle("Not Defteri")
        self.temizle.clicked.connect(self.clear)
        self.ac.clicked.connect(self.open)
        self.kaydet.clicked.connect(self.save)
        self.show()
    def clear(self):
        self.yazi.clear()
    def open(self):
        dosya = QtWidgets.QFileDialog.getOpenFileName(self,"Dosya aç",os.getenv("HOME"),"Text Files (*.txt);;all files (*)")
        with open(dosya[0],"r",encoding = "UTF-8") as file:
            self.yazi.setText(file.read())
    def save(self):
        moe = QtWidgets.QFileDialog.getSaveFileName(self,"Dosya Kaydet",os.getenv("HOME"),"Text Files (*.txt);; all files (*)")
        with open(moe[0],"w",encoding = "UTF-8") as file:
            file.write(self.yazi.toPlainText())
app = QtWidgets.QApplication(sys.argv)
pencere = pencere()
sys.exit(app.exec_())
