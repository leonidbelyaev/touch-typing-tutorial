from PyQt6 import uic
from PyQt6.QtWidgets import QDialog

from src.index import MODE_NAMES


class TypingWindow(QDialog):
    def __init__(self, mode):
        super().__init__()
        uic.loadUi("src/design/typing.ui", self)
        self.mode = mode
        self.setWindowTitle(f"{MODE_NAMES[mode.type]} — Touch Typing Tutorial")
