import sys
import os
from random import randint
from PyQt5 import (uic, QtWidgets, QtGui)
from PyQt5.Qt import (QImage, QPalette, QBrush)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui  import (QIcon, QColor)
from PyQt5.QtWidgets import (QApplication, QWidget, QListWidget, QStackedWidget,
                             QHBoxLayout, QListWidgetItem, QLabel, QTableWidgetItem, QMainWindow)


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
        self.names = os.listdir('Game') + ['Options']
        self.initUi()

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

        # Имитация 5 правых страниц



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
    ex = Launcher()
    ex.show()
    sys.exit(app.exec())
