from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
import sys

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


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
        self.addfile = QtWidgets.QPushButton(parent=self.centralwidget)
        self.addfile.setGeometry(QtCore.QRect(10, 10, 291, 181))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.addfile.setFont(font)
        self.addfile.setObjectName("addfile")
        self.addfile.setStyleSheet("background-color: transparent;")
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
        self.conv.setText(_translate("MainWindow", "Конвертировать"))


class converter(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.addfile.clicked.connect(self.run)
        self.files = []

    def run(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            '*.jpg;;*.png;;Все файлы (*)')[0]

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            if not self.files:
                self.listw = QtWidgets.QListWidget()
                self.listw.move(5, 5)
                self.listw.resize(315, 200)
                self.addfile.setText('')
            if f not in self.files:
                self.files.append(f)
                self.listw.addItem(f)
            print(f)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = converter()
    ex.show()
    sys.exit(app.exec())