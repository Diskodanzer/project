from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QPushButton, QLineEdit, QWidget, QLabel, QApplication

import sys

#const
screen_w = 1280
screen_h = 720
move_w = 750
move_h = 300
fps_counter = False

class Settings(QWidget):
    def __init__(self, prev):
        self.prev = prev
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Настройки')
        self.setStyleSheet("background-color: black")
        self.setGeometry(move_w, move_h, screen_w, screen_h)
        self.pixmap = QPixmap('resources/bg.jpeg')
        self.img = QLabel(self)
        self.img.resize(1280, 720)
        self.img = QLabel(self)
        self.img.setPixmap(self.pixmap)
        self.screen_title = QLabel(self)
        self.screen_title.move(100, 100)
        self.screen_title.setText('Размер окна:')
        self.screen_title.setStyleSheet("font-size: 30px; color: white")
        self.input_screen_w = QLineEdit(self)
        self.input_screen_w.move(350, 105)
        self.input_screen_w.resize(100, 35)
        self.input_screen_w.setStyleSheet("font-size: 30px; color: white")
        self.x = QLabel(self)
        self.x.setStyleSheet("font-size: 30px; color: white")
        self.x.setText('X')
        self.x.move(451, 100)
        self.input_screen_h = QLineEdit(self)
        self.input_screen_h.resize(100, 35)
        self.input_screen_h.setStyleSheet("font-size: 30px; color: white")
        self.input_screen_h.move(500, 105)
        self.move_title = QLabel(self)
        self.move_title.move(100, 200)
        self.move_title.setText('Сдвиг окна:')
        self.move_title.setStyleSheet("font-size: 30px; color: white")
        self.input_move_w = QLineEdit(self)
        self.input_move_w.move(350, 205)
        self.input_move_w.resize(100, 35)
        self.input_move_w.setStyleSheet("font-size: 30px; color: white")
        self.x = QLabel(self)
        self.x.setStyleSheet("font-size: 30px; color: white")
        self.x.setText('X')
        self.x.move(451, 200)
        self.input_move_h = QLineEdit(self)
        self.input_move_h.resize(100, 35)
        self.input_move_h.setStyleSheet("font-size: 30px; color: white")
        self.input_move_h.move(500, 205)
        self.fps_counter = QLabel(self)
        self.fps_counter.setStyleSheet("font-size: 30px; color: white")
        self.fps_counter.setText('Счётчик фпс:')
        self.fps_counter.resize(200, 35)
        self.fps_counter.move(100, 300)
        self.vkl_btn = QPushButton(self)
        self.vkl_btn.setText('Вкл')
        self.vkl_btn.move(350, 300)
        self.vkl_btn.resize(200, 35)
        self.vkl_btn.setStyleSheet("background-color: white; font-size: 30px")
        self.vkl_btn.clicked.connect(self.vkl)
        self.vykl_btn = QPushButton(self)
        self.vykl_btn.setText('Выкл')
        self.vykl_btn.move(600, 300)
        self.vykl_btn.resize(200, 35)
        self.vykl_btn.setStyleSheet("background-color: gray; font-size: 30px")
        self.vykl_btn.clicked.connect(self.vykl)
        self.back_btn = QPushButton(self)
        self.back_btn.setText('Назад')
        self.back_btn.move(1000, 600)
        self.back_btn.resize(200, 35)
        self.back_btn.setStyleSheet("background-color: white; font-size: 30px")
        self.back_btn.clicked.connect(self.back)

    def vkl(self):
        global fps_counter
        fps_counter = True
        self.vkl_btn.setStyleSheet("background-color: gray; font-size: 30px")
        self.vykl_btn.setStyleSheet("background-color: white; font-size: 30px")

    def vykl(self):
        global fps_counter
        fps_counter = False
        self.vykl_btn.setStyleSheet("background-color: gray; font-size: 30px")
        self.vkl_btn.setStyleSheet("background-color: white; font-size: 30px")
    
    def back(self):
        self.prev.show()