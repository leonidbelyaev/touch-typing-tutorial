from ctypes import sizeof
import os
import sys

from PyQt6 import uic
from PyQt6.QtCore import QByteArray
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QApplication, QMainWindow

from src.index import INDEX
from src.mode import Mode
from typing_window import TypingWindow

# Change working directory
os.chdir(os.path.dirname(__file__))


def load_fonts() -> None:
    """Adds fonts from src/fonts to Qt Font Database"""
    for file in os.listdir("src/fonts"):
        if os.path.isfile(f"src/fonts/{file}"):
            print(f"Loading font: {file}")
            try:
                byte_array: QByteArray = QByteArray()
                with open(f"src/fonts/{file}", mode="rb") as f:
                    byte_array.append(f.read())
                    QFontDatabase.addApplicationFontFromData(byte_array)
            except Exception:
                continue


class MyWidget(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("src/design/home.ui", self)
        self.mode = None
        self.connect()  # Connections
        load_fonts()
        self.load_options()

    def connect(self) -> None:
        self.course_btn.clicked.connect(self.start_course)
        self.random_btn.clicked.connect(self.start_random)
        self.words_btn.clicked.connect(self.start_words)
        self.texts_btn.clicked.connect(self.start_texts)

    def load_options(self) -> None:
        for lang in INDEX["languages"]:
            self.language_box.addItem(lang)
        for lay in INDEX["layouts"]:
            self.layout_box.addItem(lay)

    def start_course(self) -> None:
        self.mode: Mode = Mode(
            "course",
            language=self.language_box.currentText(),
            layout=self.layout_box.currentText(),
        )
        self.start_typing()

    def start_random(self) -> None:
        self.mode = Mode(
            "random",
            language=self.language_box.currentText(),
            layout=self.layout_box.currentText(),
        )
        self.start_typing()

    def start_words(self) -> None:
        self.mode = Mode(
            "words",
            language=self.language_box.currentText(),
            layout=self.layout_box.currentText(),
        )
        self.start_typing()

    def start_texts(self) -> None:
        self.mode: Mode = Mode(
            "texts",
            language=self.language_box.currentText(),
            layout=self.layout_box.currentText(),
        )
        self.start_typing()

    def start_typing(self) -> None:
        self.hide()
        TypingWindow(self.mode).exec()
        self.show()


def except_hook(cls, exception, traceback) -> None:
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    ex: MyWidget = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
