import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QFont, QColor, QBrush


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
        self.lesson_text.setFontPointSize(16)
        self.progress = ""
        self.cursor = self.lesson_text.textCursor()
        # Connections
        self.back_to_menu_btn.clicked.connect(self.close)
        self.quit_btn.clicked.connect(self.exit)
        self.lesson_box.valueChanged.connect(self.update_lesson)
        self.font_box.currentTextChanged.connect(self.update_font)
        self.size_box.valueChanged.connect(self.update_font)
        self.input_box.textChanged.connect(self.process_typing)
        # Start Typing
        self.load_lesson()

    def update_font(self):
        self.lesson_text.setFontFamily(self.font_box.currentText())
        self.lesson_text.setFontPointSize(self.size_box.value())
        self.lesson_text.update()
        self.update_lesson()

    def process_typing(self):
        new_char = self.input_box.text()[-1]
        i = len(self.progress) + 1
        if (
            self.lesson_text.document()
            .toPlainText()
            .find(self.progress + new_char)
            == 0
        ):
            self.progress += new_char
            self.set_underline(i)
            self.set_underline(i - 1, False)
        else:
            self.set_underline(i - 1, fcolor1="red")

    def set_underline(
        self,
        i,
        enable=True,
        fcolor1="black",
        bcolor1="yellow",
        fcolor2="green",
        bcolor2="transparent",
    ):
        self.cursor.setPosition(i)
        self.cursor.setPosition(i + 1, QTextCursor.MoveMode.KeepAnchor)
        y = self.cursor.charFormat()
        if enable:
            y.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SingleUnderline)
            y.setFontWeight(QFont.Weight.Bold)
            y.setForeground(QBrush(QColor(fcolor1)))
            y.setBackground(QBrush(QColor(bcolor1)))
        else:
            y.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)
            y.setFontWeight(QFont.Weight.Normal)
            y.setForeground(QBrush(QColor(fcolor2)))
            y.setBackground(QBrush(QColor(bcolor2)))
        self.cursor.setCharFormat(y)

    def exit(self):
        self.hide()
        sys.exit(0)

    def update_lesson(self):
        self.input_box.setText("")
        self.progress = ""
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
        self.set_underline(0)
        self.input_box.setFocus()
