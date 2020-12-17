import sqlite3
import sys
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.Qt import QImage
from PyQt5.Qt import QSize
from PyQt5.Qt import QPalette
from PyQt5.Qt import QBrush
from PyQt5.Qt import QIcon
from PyQt5.QtGui import QColor


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


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/Launcher.ui', self)
        self.setWindowTitle('Launcher')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Start_Window()
    ex.show()
    sys.exit(app.exec())
