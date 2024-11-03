from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap
import sys
from PIL import Image
import os


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(325, 310)
        MainWindow.setFixedSize(325, 310)
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

        self.add_folder = QtWidgets.QPushButton(parent=self.centralwidget)
        self.add_folder.setGeometry(QtCore.QRect(165, 10, 150, 180))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.add_folder.setFont(font)
        self.add_folder.setObjectName("addfile")
        self.add_folder.setStyleSheet("background-color: transparent;")

        self.another_file = QtWidgets.QPushButton(parent=self.centralwidget)
        self.another_file.setGeometry(QtCore.QRect(5, 180, 300, 30))
        self.another_file.setObjectName("another_file")
        self.another_file.setStyleSheet("background-color: transparent;")
        self.another_file.hide()

        self.scroll_area = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scroll_area.setGeometry(QtCore.QRect(5, 5, 320, 175))
        self.scroll_area.setObjectName('scroll_area')
        self.scroll_area.setStyleSheet("background-color: transparent;")
        self.scroll_area.hide()

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
        self.add_folder.setText(_translate("MainWindow", "+Папка"))
        self.another_file.setText(_translate("MainWindow", "Выбрать другой файл"))
        self.conv.setText(_translate("MainWindow", "Конвертировать"))



class converter(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.files = []
        self.extensions = [
            "BMP", "ESP", "GIF", "IM",
            "JPEG", "JPG", "MSP", "PCX",
            "PNG", "PPM", "TIFF", "WEBP",
            "ICO", "PSD", "TIF", "FAX"]
        self.addformat()
        self.code.addItem('utf-8')
        self.addfile.clicked.connect(self.file)
        self.another_file.clicked.connect(self.reset)
        self.add_folder.clicked.connect(self.folder)
        self.conv.setEnabled(False)
        self.conv.clicked.connect(self.convert)

    def addformat(self):
        self.format.addItems(self.extensions)

    def file(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать файл', '',
            '*.jpg;;*.png;;*.bmp;;*.esp;;*.gifim;;*.jpeg;;*.msp;;*.pcx;'
            ';*.ppm;;*.tiff;;*.webp;;*.ico;;*.psd;;*.tif;;*.fax;;Все файлы (*)')[0]
        if fname != '':
            self.files.append(fname)
            self.first()
            print(self.files)

    def folder(self, fname=False):
        if not fname:
            fname = QFileDialog.getExistingDirectory(self, 'Выбрать папку')
        for f in os.listdir(fname):
            if f.split('.')[-1].upper() in self.extensions:
                self.files.append(f'{fname}/{f}')
        self.first()
        print(self.files)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and not self.add_folder.isHidden():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            if os.path.isdir(f):
                break
        else:
            for f in files:
                if f not in self.files:
                    self.files.append(f)
                print(f)
            self.first()
            return None
        if len(files) > 1:
            pass
        else:
            self.folder(files[0])

    def first(self):
        self.addfile.hide()
        self.add_folder.hide()
        self.another_file.show()
        self.preview()
        self.conv.setEnabled(True)

    def reset(self):
        self.files = []
        self.image.hide()
        self.addfile.show()
        self.add_folder.show()
        self.another_file.hide()
        self.scroll_area.hide()

    def preview(self):
        if len(self.files) == 1:
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
        else:
            self.scroll_area.show()
            layout = QVBoxLayout()
            widget = QWidget()
            for f in self.files:
                try:
                    image = QLabel()
                    self.pixmap = QPixmap(f)
                    q = str(self.pixmap.size()).split("(")[1][:-1].split(", ")
                    if int(q[1]) > 175:
                        self.pixmap = self.pixmap.scaledToHeight(175)
                        q = str(self.pixmap.size()).split("(")[1][:-1].split(", ")
                    if int(q[0]) > 300:
                        self.pixmap = self.pixmap.scaledToWidth(300)
                    image.resize(self.pixmap.size())
                    image.setPixmap(self.pixmap)
                    layout.addWidget(image)
                except Exception:
                    pass
            widget.setLayout(layout)
            self.scroll_area.setWidget(widget)

    def convert(self):
        self.open = Second_Window()
        self.open.send_data.connect(self.dir)
        self.open.show()
        self.conv_im()

    def conv_im(self):
        pass

    def dir(self, data):
        print(data)

class Second_Window(QWidget):
    send_data = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(325, 80)
        self.setFixedSize(325, 80)
        self.setWindowTitle('Сохранить в')
        self.path = QLineEdit(self)
        self.path.move(5, 10)
        self.path.resize(315, 20)

        self.choose = QPushButton('Выбрать', self)
        self.choose.move(175, 35)
        self.choose.resize(70, 20)
        self.choose.clicked.connect(self.folder)

        self.fname = None
        self.ok = QPushButton('OK', self)
        self.ok.move(250, 35)
        self.ok.resize(70, 20)
        self.ok.clicked.connect(self.send)

    def send(self):
        self.send_data.emit(self.fname)
        self.close()

    def folder(self):
        self.fname = QFileDialog.getExistingDirectory(self, 'Выбрать папку')
        self.path.setText(self.fname)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = converter()
    ex.show()
    sys.exit(app.exec())