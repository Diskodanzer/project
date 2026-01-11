from PyQt6.QtWidgets import QPushButton, QWidget, QApplication, QLabel
from PyQt6.QtGui import QPixmap

import sys

from pycode.Settings_window import Settings
from pycode.prototype import GridGame

#consts
screen_w = 1280
screen_h = 720
move_w = 750
move_h = 300


class Main_window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('vymluva')
        self.setGeometry(move_w, move_w, screen_w, screen_h)
        self.pixmap = QPixmap('resources/bg.jpeg')
        self.img = QLabel(self)
        self.img.resize(1280, 720)
        self.img.setPixmap(self.pixmap)
        self.start_btn = QPushButton(self)
        self.start_btn.setText('Начать')
        self.start_btn.resize(525, 100)
        self.start_btn.move(350, 150)
        self.start_btn.clicked.connect(self.start)
        self.settings_btn = QPushButton(self)
        self.settings_btn.setText('Настройки')
        self.settings_btn.resize(525, 100)
        self.settings_btn.move(350, 300)
        self.settings_btn.clicked.connect(self.settings)

    def start(self):
        self.start_form = GridGame(self, None)
        self.start_form.show()

    def settings(self):
        self.settings_form = Settings(self, None)
        self.settings_form.show()
