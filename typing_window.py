import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog


from src.index import MODE_NAMES

# Adding Roboto Mono


def load_lesson_text(i, mode):
    filename = "src/lessons/"
    if mode.type == "course":
        filename += f"course/{mode.layout}/{i}.txt"
    elif mode.type == "random":
        filename += f"random/{mode.layout}.txt"
    elif mode.type == "words":
        filename += f"words/{mode.language}.txt"
    elif mode.type == "texts":
        filename += f"texts/{mode.language}/{i}.txt"
    try:
        print("Loading " + filename)
        with open(filename, encoding="utf-8", mode="r") as f:
            return f.read()
    except FileNotFoundError:
        return None


class TypingWindow(QDialog):
    def __init__(self, mode):
        super().__init__()
        uic.loadUi("src/design/typing.ui", self)
        self.mode = mode
        self.setWindowTitle(f"{MODE_NAMES[mode.type]} — Touch Typing Tutorial")
        self.lesson_text.setFontFamily("Roboto Mono")
        # Connections
        self.back_to_menu_btn.clicked.connect(self.close)
        self.quit_btn.clicked.connect(self.exit)
        self.lesson_box.valueChanged.connect(self.update_lesson)
        self.font_box.currentTextChanged.connect(self.update_font)
        self.size_box.valueChanged.connect(self.update_font)
        # Start Typing
        self.load_lesson()

    def update_font(self):
        self.lesson_text.setFontFamily(self.font_box.currentText())
        self.lesson_text.setFontPointSize(self.size_box.value())
        self.lesson_text.update()
        self.update_lesson()

    def exit(self):
        self.hide()
        sys.exit(0)

    def update_lesson(self):
        self.input_box.setText("")
        self.load_lesson()

    def load_lesson(self):
        t = load_lesson_text(self.lesson_box.text(), self.mode)
        if t is None:
            self.lesson_text.setText(
                "This lesson does not exist. "
                "Please, try another, or add it manually."
            )
            return
        if self.mode.type in ["course", "texts"]:
            self.lesson_text.setText(t)
