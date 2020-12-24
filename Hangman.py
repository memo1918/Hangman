# pyinstaller --onefile --noconsole Hangman.py
from PyQt5 import QtGui,QtWidgets
import sys
import random

class Hangman(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.UI()
        self.basla()
        #a kala hakkin kazanma kazanmaya olan yakinligin yh ise yazidigin harfler
        self.a = 0
        self.kazanma = 0
        self.yh = [""," "]

    def UI(self):
        #resimleri daha kolay değiştirmek için
        self.resim_liste = ["start.png","pahase1.png","pahase2.png","pahase3.png","pahase4.png","gameover.png"]
        #resımlerı koydugum alan
        self.alan = QtWidgets.QLabel()
        #kelimenin cikacagi veya ilerlemenin gosterldigi yer
        self.kelime = QtWidgets.QLabel("")
        #sana durumunu soyler
        self.kernel = QtWidgets.QLabel("")
        self.restart = QtWidgets.QPushButton("Restart")
        self.enter = QtWidgets.QPushButton("Enter")
        #yazi yazdigin yer
        self.yazi = QtWidgets.QLineEdit()

        self.hbox= QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.enter)
        self.hbox.addWidget(self.restart)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.alan)
        self.vbox.addWidget(self.kelime)
        self.vbox.addWidget(self.kernel)
        self.vbox.addWidget(self.yazi)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)
        self.restart.clicked.connect(self.Restart)
        self.enter.clicked.connect(self.Enter)
        self.show()

    def Restart(self):
        self.kazanma = 0
        self.a = 0
        self.yh = [""," "]
        self.basla()
        self.kernel.setText("")

    def Enter(self):
        while True:
            #2 karakterden fazla girmeni engeliyor
            if len(self.yazi.text()) >= 2:
                self.yazi.clear()
                break
            #daha once girdigin bir harfi girmeni engelliyor
            elif self.yh.count(self.yazi.text()) >= 1:
                self.yazi.clear()
                self.kernel.setText("Bu harfi daha once denedin")
                break
            #tahminin dogruysaburdasin
            elif self.rastgelek.count(self.yazi.text()) >= 1:
                #tahmin edilen kelimelere ekliyor ve yazi yazdiriyuor
                self.yh.append(self.yazi.text())
                self.kernel.setText("Harika bu harften {} tane var".format(self.rastgelek.count(self.yazi.text())))
                #bu kisimda tahmin edilen harfleri gosteriyor
                #oncelikle daha once koydugumuz '/' lari listeye ceviriyor
                #sonra kelimemizdeki elemenlari indexleyerek bir listeye atiyor (enumerate)
                #bu listenin icindeki harfleri tariyor eger tahmin edilen harf dogruysa
                #indices listesine bu harfin indexini yani konumuu atiyor
                #yazilan harfin verisi zaten bizde oldugu ve indices listesindede bu harfin gercekte hangi
                #indexe ait oldugunu bildimiz icin worc_list yani '/' larin listesindeki buldugumuz
                #indexin yerini harfle degistiriyoruz sonrada wrod_c ye esitliyoruz
                wordc_list = list(self.word_c)
                indices = [i for i, letter in enumerate(self.rastgelek) if letter == self.yazi.text()]
                for i in indices:
                    wordc_list[i] = self.yazi.text()
                self.word_c ="".join(wordc_list)
                self.kelime.setText(self.word_c)
                #kazanma sayacina ekleme yapip kazanip kazanmadigini konrtol ediyor
                self.kazanma += self.rastgelek.count(self.yazi.text())
                if self.kazanma == len(self.rastgelek):
                    self.Kazanma()
                self.yazi.clear()
                break
            else:
                #yanlis tahmin etmissen burdasin hak eksiltir resim degistirir
                self.yh.append(self.yazi.text())
                self.a += 1
                self.yazi.clear()
                self.kernel.setText("Bilemedin {} hakkin kaldi".format(5-self.a))
                self.alan.setPixmap(QtGui.QPixmap(self.resim_liste[self.a]))
                #bu if kaybetmeni kontrol ediyor
                if self.a == 5:
                    self.kernel.setText("Hakkiniz kalmadi")
                    self.kelime.setText(self.rastgelek)
                break

    def basla(self):
        #kisaca txt yi acar ve rastgele bir kelime secer
        with open("kelimeler2.txt","r",encoding="utf-8") as kfile:
            liste = kfile.read().strip("\n").splitlines()
            self.rkureten = liste[random.randint(0,1070)]
            self.rastgelek = self.rkureten
        self.alan.setPixmap(QtGui.QPixmap(self.resim_liste[0]))
        #bu 2 satirda kelimenin uzunlugu kadar '/' koyuyor
        self.word_c = "/" * len(self.rastgelek)
        self.kelime.setText(self.word_c)
        self.yazi.clear()

    def Kazanma(self):
        self.kernel.setText("Kazandin")
        self.kelime.setText(self.rastgelek)

#burdaki kodlar arayuz icin sart
app = QtWidgets.QApplication(sys.argv)
#bu kod font size i ayarliyor
app.setStyleSheet("QLabel{font-size: 18pt;}")
oyun = Hangman()
sys.exit(app.exec_())
