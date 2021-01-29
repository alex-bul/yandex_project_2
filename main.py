import sqlite3
import sys
import os
import subprocess
from PyQt5 import (uic, QtWidgets, QtGui)
from PyQt5.Qt import (QImage, QPalette, QBrush)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import (QIcon, QColor)
from PyQt5.QtWidgets import (QApplication, QWidget, QListWidget, QStackedWidget,
                             QHBoxLayout, QListWidgetItem, QLabel, QTableWidgetItem, QMainWindow)


class Start_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/Start Window.ui', self)
        self.setWindowTitle('Entry')
        self.btn_sign_up.clicked.connect(self.registration)
        self.btn_sign_in.clicked.connect(self.enter)
        self.btn_guest.clicked.connect(self.guest)

    def get_data(self):
        pass

    def registration(self):
        self.get_data()

        con = sqlite3.connect("Res/data.db")
        cur = con.cursor()

        id = list(cur.execute("""SELECT max(id) FROM data""").fetchone())[0] + 1
        logins = [str(list(i)[0]) for i in cur.execute("""SELECT login FROM data""").fetchall()]
        nicks = [str(list(i)[0]) for i in cur.execute("""SELECT user_name FROM data""").fetchall()]

        name = str(self.user_name.text().strip())
        login = str(self.login.text().strip())
        password_1 = str(self.password.text().strip())
        password_2 = str(self.confirm_password.text().strip())

        if password_1 != password_2:
            self.error.setText("Passwords don't match")
        elif login in logins:
            self.error.setText('The login is already taken')
        elif name in nicks:
            self.error.setText('Еhe username is already taken')
        elif name == '':
            self.error.setText('User name has empty')
        elif login == '':
            self.error.setText('Login has empty')
        elif password_1 == '':
            self.error.setText('Password has empty')
        else:
            self.error.setText('')
            cur.execute(f"""INSERT INTO data
                    VALUES('{id}', '{name}','{login}', '{password_1}', '{0}')""")
            self.tabWidget.setCurrentIndex(0)

        con.commit()
        con.close()

    def enter(self):
        con = sqlite3.connect("Res/data.db")
        cur = con.cursor()

        logins = [str(list(i)[0]) for i in cur.execute("""SELECT login FROM data""").fetchall()]

        login = str(self.ent_login.text().strip())
        password = str(self.ent_pass.text().strip())
        if login == '':
            self.error_2.setText('Login has empty')
        elif password == '':
            self.error_2.setText('Password has empty')
        elif login not in logins or password != str(
                cur.execute(f"""SELECT * FROM data where login = '{login}'""").fetchone()[3]):
            self.error_2.setText('Invalid login or password')
        else:
            self.error_2.setText('')
            result = list(cur.execute(f"""SELECT * FROM data where login = '{login}'""").fetchone())
            print(result)
            with open('user data.txt', 'w') as f:
                f.write(str(result))
            self.close()
            self.launcher = Launcher()
            self.launcher.show()

    def guest(self):
        with open('user data.txt', 'w') as f:
            f.write('["None", "Guest", "None", "None", 0]')
        self.close()
        self.launcher = Launcher()
        self.launcher.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/Launcher.ui', self)
        self.setWindowTitle('Launcher')
        self.resize(800, 600)
        # Левый и правый макет (один QListWidget слева + QStackedWidget справа)
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        # QListWidget слева
        print(os.listdir('Game'))
        self.names = os.listdir('Game')
        self.initUi()
        self.Crazy_Fox.setStyleSheet("background-image: url(Res/Crazy Fox.png)")
        self.Dungeon.setStyleSheet("background-image: url(Res/Dungeon.png)")
        self.Wheel.setStyleSheet("background-image: url(Res/Wheel.png)")
        self.SovietEmpire.setStyleSheet("background-image: url(Res/SovietEmpire.png)")
        self.Play_Fox.clicked.connect(self.fox)
        self.Play_Dungeon.clicked.connect(self.dungeon)
        self.Play_Wheel.clicked.connect(self.wheel)
        print(1)
        try:
            self.Play_SovietEmpire.clicked.connect(self.soviet)
        except Exception as e:
            print(e)
        data = eval(open('user data.txt', 'r').read())
        self.User.setText(f'Hello {data[1]}')
        print(1)
        self.Coin.setText(f'Coins: {data[-1]}')
        self.dun = False

    def initUi(self):
        # Интерфейс инициализации
        # Переключить порядковый номер в QStackedWidget на текущее изменение элемента QListWidget
        self.listWidget.currentRowChanged.connect(
            self.stackedWidget.setCurrentIndex)

        # Удалить border
        self.listWidget.setFrameShape(QListWidget.NoFrame)
        # Скрыть полосу прокрутки
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Здесь мы используем общий текст с режимом значков
        # (вы также можете использовать режим значков, setViewMode напрямую)
        for i in self.names:
            item = QListWidgetItem(str(i), self.listWidget)
            # Установите ширину и высоту элемента по умолчанию (здесь полезна только высота)
            item.setSizeHint(QSize(16777215, 60))
            # Текст по центру
            item.setTextAlignment(Qt.AlignCenter)

    def fox(self):
        subprocess.Popen('cmd.exe /c start' + f" {os.path.abspath('Game/CrazyFox/main.pyw')}", shell=False)

    def dungeon(self):
        self.dungeon = Dungeon()
        self.dungeon.show()
        self.dun = True
        self.close()

    def soviet(self):
        subprocess.Popen('cmd.exe /c start' + f" {os.path.abspath('Game/SovietEmpire/main.pyw')}", shell=True)
        print(1)

    def wheel(self):
        subprocess.Popen('cmd.exe /c start' + f" {os.path.abspath('Game/Wheel/main.pyw')}", shell=True)
        print(1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
            self.start_window = Start_Window()
            self.start_window.show()

    def closeEvent(self, event):
        self.close()
        if not self.dun:
            self.start_window = Start_Window()
            self.start_window.show()


class Dungeon(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/Join_to_dungeon.ui', self)
        self.setWindowTitle('Join to Dungeon')
        self.btn_Play.clicked.connect(self.enter)
        self.btn_Free.clicked.connect(self.guest)

    def enter(self):
        con = sqlite3.connect("Res/data.db")
        cur = con.cursor()
        logins = [str(list(i)[0]) for i in cur.execute("""SELECT login FROM data""").fetchall()]
        login_1 = str(self.login_Player_1.text().strip())
        login_2 = str(self.login_Player_2.text().strip())
        password_1 = str(self.pass_Player_1.text().strip())
        password_2 = str(self.pass_Player_2.text().strip())

        if login_1 == '' or login_2 == '':
            self.error.setText('Login has empty')
        elif login_1 == login_2:
            self.error.setText('The logins are the same')
        elif password_1 == '' or password_2 == '':
            self.error.setText('Password has empty')
        elif (login_1 not in logins or login_2 not in logins) or (password_1 != str(
                cur.execute(f"""SELECT pass FROM data where login = '{login_1}'""").fetchall()[0][0]) \
                                                                  or password_2 != str(
                    cur.execute(f"""SELECT pass FROM data where login = '{login_2}'""").fetchall()[0][0])):
            self.error.setText('Invalid login or password')
        else:
            self.error.setText('')
            self.run(login_1, login_2)

    def guest(self):
        print(1)
        os.system('python ' + f"{os.path.abspath('Game/Dungeon/main.pyw')}")

    def run(self, login_1, login_2):
        print(1)
        os.system('python ' + f"{os.path.abspath('Game/Dungeon/main.pyw')} {self.bet.value()} {login_1} {login_2}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.launcher = Launcher()
            self.launcher.show()
            self.close()

    def closeEvent(self, event):
        self.close()
        self.launcher = Launcher()
        self.launcher.show()


# style sheet
Stylesheet = """
QListWidget, QListView, QTreeWidget, QTreeView {
    outline: 2px;
}
QListWidget {
    min-width: 150px;
    max-width: 150px;
}
QListWidget::item:selected {
    border-left: 2px solid rgb(9, 187, 7);"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Start_Window()
    ex.show()
    sys.exit(app.exec())
