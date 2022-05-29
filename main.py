import os
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

from src.connections import Connections
import typing
from typing_window import TypingWindow
from src.mode import Mode

# Сhange working directory
cur_dir = os.path.dirname(__file__)
os.chdir(cur_dir)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/design/home.ui", self)
        # Connections
        self.connect()

    def connect(self):
        self.course_btn.clicked.connect(self.start_course)
        self.random_btn.clicked.connect(self.start_random)
        self.words_btn.clicked.connect(self.start_words)
        self.texts_btn.clicked.connect(self.start_texts)

    def start_course(self):
        self.mode = Mode(
            "course",
            language=self.language_box.currentText(),
            layout=self.layout_box.currentText(),
        )
        self.start_typing()

    def start_random(self):
        self.mode = Mode(
            "random",
            language=self.language_box.currentText(),
            layout=self.layout_box.currentText(),
        )
        self.start_typing()

    def start_words(self):
        self.mode = Mode(
            "words",
            language=self.language_box.currentText(),
            layout=self.layout_box.currentText(),
        )
        self.start_typing()

    def start_texts(self):
        self.mode = Mode(
            "texts",
            language=self.language_box.currentText(),
            layout=self.layout_box.currentText(),
        )
        self.start_typing()

    def start_typing(self, mode=None):
        if mode is None:
            mode = self.mode
        t = TypingWindow(mode)
        self.hide()
        t.exec()
        self.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
