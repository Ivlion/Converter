from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QVBoxLayout, QWidget, QLineEdit, \
    QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QPixmap
import sys
from PIL import Image
import os
import csv
import sqlite3
import datetime


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
        self.addfile.setObjectName("addfile")
        self.addfile.setStyleSheet("background-color: transparent;")

        self.add_folder = QtWidgets.QPushButton(parent=self.centralwidget)
        self.add_folder.setGeometry(QtCore.QRect(165, 10, 150, 180))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.add_folder.setFont(font)
        self.add_folder.setObjectName("add_folder")
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
        self.conv.setGeometry(QtCore.QRect(210, 260, 100, 30))
        self.conv.setObjectName("conv")

        self.history = QtWidgets.QPushButton(parent=self.centralwidget)
        self.history.setGeometry(QtCore.QRect(210, 210, 100, 30))
        self.history.setObjectName("history")

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
        self.history.setText(_translate("MainWindow", "История"))



class Converter(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.st_inf = {}
        self.start()
        self.setAcceptDrops(True)
        self.files = []
        self.extensions = [
            "BMP", "ESP", "GIF", "IM",
            "JPEG", "MSP", "PCX",
            "PNG", "PPM", "TIFF", "WEBP",
            "ICO", "PSD", "FAX", "PDF"]
        self.addformat()
        self.format.currentIndexChanged.connect(self.chng_format)
        self.code.addItem('utf-8')
        self.addfile.clicked.connect(self.file)
        self.another_file.clicked.connect(self.reset)
        self.add_folder.clicked.connect(self.folder)
        self.conv.setEnabled(False)
        self.conv.clicked.connect(self.convert)
        self.final_dir = None
        self.history.clicked.connect(self.show_table)

    def show_table(self):
        self.openh = Table()
        self.openh.show()

    def start(self):
        with open('start.csv', encoding="utf8") as csvfile:
            reader = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
            for i in range(len(reader[0])):
                self.st_inf[reader[0][i]] = reader[1][i]
            print(self.st_inf)

    def closeEvent(self, e):
        self.save()

    def save(self):
        print(self.st_inf)
        with open('start.csv', 'w', newline='', encoding="utf8") as f:
            writer = csv.DictWriter(
                f, fieldnames=self.st_inf.keys(),
                delimiter=',', quoting=csv.QUOTE_NONNUMERIC, quotechar='"')
            writer.writeheader()
            writer.writerow(self.st_inf)

    def addformat(self):
        self.format.addItems(self.extensions)
        self.format.setCurrentIndex(int(self.st_inf['last_format']))

    def chng_format(self):
        self.st_inf['last_format'] = str(self.format.currentIndex())

    def file(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать файл', '',
            'Изображения (*.jpg;*.png;*.bmp;*.esp;*.gifim;*.jpeg;*.msp;*.pcx;'
            '*.ppm;*.tiff;*.webp;*.ico;*.psd;*.tif;*.fax);;Все файлы (*)')[0]
        if fname != '':
            self.files.append(fname)
            self.first()
            print(self.files)

    def folder(self, fname=False):
        if not fname:
            fname = QFileDialog.getExistingDirectory(self, 'Выбрать папку')
        if fname != '':
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
        self.conv.setEnabled(False)

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

    def conv_im(self):
        for el in self.files:
            if el.split('.')[-1].lower() not in ["gif", "tiff", "tif"]:
                try:
                    lst = self.one_page(el)
                    print(el, lst)
                    self.write_history(el, '\n'.join(lst), 'OK')
                except Exception as e:
                    self.write_history(el, 'None', str(type(e).__name__ ) + ':'+ str(e))
                    raise e
            else:
                try:
                    lst = self.multy_page(el)
                    self.write_history(el, '\n'.join(lst), 'OK')
                except Exception as e:
                    self.write_history(el, 'None', str(type(e).__name__ ) + ':'+ str(e))

    def write_history(self, of, ff, log):
        print("OK")
        con = sqlite3.connect("history.sqlite")
        cur = con.cursor()
        cur.execute(f"""INSERT INTO history(date_time, original_file, final_file, log) 
                        VALUES (?, ?, ?, ?)
                    """, (str(datetime.datetime.now()), of, ff, log))
        con.commit()

    def dir(self, data):
        self.final_dir = data
        self.st_inf['last_save'] = data
        self.save()
        print(data)
        self.conv_im()
        self.reset()

    def one_page(self, im):
        form = self.format.currentText().lower()
        print(form)
        lst = []
        image = Image.open(im)
        i = 0
        image.convert("RGB")
        image.seek(i)
        image.save(f"{self.new_name(im)}.{form}", format=form)
        lst.append(f"{self.new_name(im)}.{form}")
        while True:
            i += 1
            try:
                image.seek(i)
                image.save(f"{self.new_name(im)}({i + 1}).{form}", format=form)
                lst.append(f"{self.new_name(im)}({i + 1}).{form}")
            except EOFError:
                break
        image.close()
        return lst

    def multy_page(self, im):
        lst = []
        form = self.format.currentText().lower()
        img = Image.open(im)
        s = []
        name = ""
        for el in im.split("/")[:-1]:
            name += el + "/"
        i = 0
        a = []
        img.seek(i)
        img.save(f"{name}asd.png", "png")
        s.append(Image.open(f"{name}asd.png"))
        a.append(f"{name}asd.png")
        lst.append(f"{name}asd.png")
        while True:
            i += 1
            try:
                img.seek(i)
                img.save(f"{name}asd{i}.png", "png")
                s.append(Image.open(f"{name}asd{i}.png"))
                a.append(f"{name}asd{i}.png")
                lst.append(f"{name}asd{i}.png")
            except EOFError:
                break
            except Exception as e:
                for el in a:
                    os.unlink(el)
                return e
        s[0].save(
            f"{self.new_name(im)}.{form}",
            form,
            save_all=True,
            append_images=s[1:],
        )
        img.close()
        for el in a:
            os.unlink(el)
        return lst

    def new_name(self, im):
        return self.final_dir + im[im.rfind('/'): im.rfind('.')] + '_converted'


class Second_Window(QMainWindow):
    send_data = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(325, 80)
        self.setFixedSize(325, 80)
        self.setWindowTitle('Сохранить в')

        self.st_inf = {}
        self.start()

        self.ok = QPushButton('OK', self)

        self.path = QLineEdit(self)
        self.path.move(5, 10)
        self.path.resize(315, 20)
        self.path.setText(self.st_inf['last_save'])
        self.path_changed()

        self.choose = QPushButton('Выбрать', self)
        self.choose.move(175, 35)
        self.choose.resize(70, 20)
        self.choose.clicked.connect(self.folder)

        self.fname = None
        self.ok.move(250, 35)
        self.ok.resize(70, 20)
        self.ok.clicked.connect(self.send)

        self.path.textChanged.connect(self.path_changed)

    def start(self):
        with open('start.csv', encoding="utf8") as csvfile:
            reader = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
            for i in range(len(reader[0])):
                self.st_inf[reader[0][i]] = reader[1][i]
            if self.st_inf['last_save'] == '0':
                self.st_inf['last_save'] = '/'.join(os.getcwd().split('\\'))
            print(self.st_inf)

    def send(self):
        if not self.fname:
            self.fname = self.st_inf['last_save']
        self.send_data.emit(self.fname)
        self.close()

    def folder(self):
        self.fname = QFileDialog.getExistingDirectory(self, 'Выбрать папку')
        self.path.setText(self.fname)

    def path_changed(self):
        self.fname = self.path.text()
        if os.path.exists(self.fname):
            self.statusBar().setStyleSheet('color:green')
            self.statusBar().showMessage('Указанный путь существует')
            self.ok.setEnabled(True)
        else:
            self.statusBar().setStyleSheet('color:red')
            self.statusBar().showMessage('Указанный путь не существует')
            self.ok.setEnabled(False)

class Table(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(500, 400)
        self.setFixedSize(500, 415)
        self.setWindowTitle('История')

        self.con = sqlite3.connect("history.sqlite")
        self.selected_item = QLineEdit(self)
        self.selected_item.move(5, 370)
        self.selected_item.resize(400, 25)

        self.table = QTableWidget(self)
        self.table.resize(490, 360)
        self.table.move(5, 5)
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.cellClicked.connect(self.show_item)

        self.clear = QPushButton('Очистить', self)
        self.clear.move(410, 368)
        self.clear.resize(80, 30)
        self.clear.clicked.connect(self.clear_table)

        self.update_result()

    def clear_table(self):
        cur = self.con.cursor()
        cur.execute("DELETE FROM history")
        self.con.commit()
        self.table.clear()
        self.update_result()

    def show_item(self, row, column):
        self.selected_item.setText(self.table.item(row, column).text())

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM history").fetchall()
        self.table.setColumnCount(4)
        titles = [description[0] for description in cur.description][1:]
        self.table.setHorizontalHeaderLabels(titles)
        if not result:
            self.statusBar().showMessage('Вы ничего не конвертировали')
            return
        self.table.setRowCount(len(result))
        print(result)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem[1:]):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Converter()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())