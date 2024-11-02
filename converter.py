from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtGui import QPixmap
import sys
from PIL import Image

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

X, Y = 325, 310

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(325, 310)
        MainWindow.setMinimumSize(QtCore.QSize(325, 300))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 200, 201, 101))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.format = QtWidgets.QComboBox(parent=self.gridLayoutWidget)
        self.format.setObjectName("format")
        self.gridLayout.addWidget(self.format, 0, 1, 1, 1)
        self.code = QtWidgets.QComboBox(parent=self.gridLayoutWidget)
        self.code.setObjectName("code")
        self.gridLayout.addWidget(self.code, 1, 1, 1, 1)

        self.image = QtWidgets.QLabel(parent=self.centralwidget)
        self.image.setObjectName("image")
        self.image.move(5, 5)
        self.image.raise_()
        self.image.hide()

        self.addfile = QtWidgets.QPushButton(parent=self.centralwidget)
        self.addfile.setGeometry(QtCore.QRect(10, 10, 150, 180))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.addfile.setFont(font)
        self.addfile.setObjectName("adddir")
        self.addfile.setStyleSheet("background-color: transparent;")

        self.adddir = QtWidgets.QPushButton(parent=self.centralwidget)
        self.adddir.setGeometry(QtCore.QRect(165, 10, 150, 180))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.adddir.setFont(font)
        self.adddir.setObjectName("addfile")
        self.adddir.setStyleSheet("background-color: transparent;")

        self.another_file = QtWidgets.QPushButton(parent=self.centralwidget)
        self.another_file.setGeometry(QtCore.QRect(5, 180, 300, 30))
        self.another_file.setObjectName("defolt")
        self.another_file.setStyleSheet("background-color: transparent;")
        self.another_file.hide()

        self.conv = QtWidgets.QPushButton(parent=self.centralwidget)
        self.conv.setGeometry(QtCore.QRect(210, 260, 101, 31))
        self.conv.setObjectName("conv")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 325, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Конвертер"))
        self.label.setText(_translate("MainWindow", "Конвертировать в:"))
        self.label_2.setText(_translate("MainWindow", "Кодировка:"))
        self.addfile.setText(_translate("MainWindow", "+Файл"))
        self.adddir.setText(_translate("MainWindow", "+Папка"))
        self.another_file.setText(_translate("MainWindow", "Выбрать другой файл"))
        self.conv.setText(_translate("MainWindow", "Конвертировать"))



class converter(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.addformat()
        self.code.addItem('utf-8')
        self.addfile.clicked.connect(self.run)
        self.another_file.clicked.connect(self.reset)
        self.files = []

    def addformat(self):
        self.format.addItems([
            "BMP", "ESP", "GIF", "IM",
            "JPEG", "JPG", "MSP", "PCX",
            "PNG", "PPM", "TIFF", "WEBP",
            "ICO", "PSD", "TIF", "FAX"])

    def run(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать файл', '',
            '*.jpg;;*.png;;*.bmp;;*.esp;;*.gifim;;*.jpeg;;*.msp;;*.pcx;'
            ';*.ppm;;*.tiff;;*.webp;;*.ico;;*.psd;;*.tif;;*.fax;;Все файлы (*)')[0]
        if fname != '':
            self.files.append(fname)
            self.first()
            self.preview()
            print(self.files)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            if not self.files:
                self.files.append(f)
                self.first()
            elif f not in self.files:
                self.files.append(f)
            print(f)

    def first(self):
        self.addfile.hide()
        self.adddir.hide()
        self.another_file.show()
        self.preview()

    def reset(self):
        self.files = []
        self.image.hide()
        self.addfile.show()
        self.adddir.show()
        self.another_file.hide()

    def preview(self):
        self.image.show()
        try:
            self.pixmap = QPixmap(self.files[0])
            q = str(self.pixmap.size()).split("(")[1][:-1].split(", ")
            if int(q[1]) > 175:
                self.pixmap = self.pixmap.scaledToHeight(175)
                q = str(self.pixmap.size()).split("(")[1][:-1].split(", ")
            if int(q[0]) > 300:
                self.pixmap = self.pixmap.scaledToWidth(300)
            self.image.resize(self.pixmap.size())
            self.image.setPixmap(self.pixmap)
        except Exception:
            pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = converter()
    ex.show()
    sys.exit(app.exec())