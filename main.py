import os
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

# Сhange working directory
cur_dir = os.path.dirname(__file__)
os.chdir(cur_dir)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/design/home.ui", self)
        # Your code


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
