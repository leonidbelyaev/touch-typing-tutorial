import sys
import random

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QFont, QColor, QBrush


from src.index import MODE_NAMES
from src.mode import Mode

# Adding Roboto Mono


def load_lesson_text(i, mode: Mode) -> str | None:
    filename: str = "src/lessons/"
    if mode.type == "course":
        filename += f"course/{mode.layout}/{i}.txt"
    elif mode.type == "random":
        filename += f"random/{mode.layout}.txt"
    elif mode.type == "words":
        filename += f"words/{mode.language}.txt"
    elif mode.type == "texts":
        filename += f"texts/{mode.language}/{i}.txt"
    try:
        print("Loading lesson: " + filename)
        with open(filename, encoding="utf-8", mode="r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def get_ways(ls: list) -> list:
    ways = []
    if len(ls) == 1:
        return ls[0]
    for i in ls:
        ls2 = ls.copy()
        del ls2[ls2.index(i)]
        for way in get_ways(ls2):
            ways.append([i, *way])
    return ways


class TypingWindow(QDialog):
    def __init__(self, mode: Mode) -> None:
        super().__init__()
        uic.loadUi("src/design/typing.ui", self)  # type: ignore
        self.mode: Mode = mode
        self.setWindowTitle(f"{MODE_NAMES[mode.type]} — Touch Typing Tutorial")
        self.lesson_text.setFontFamily("Roboto Mono")
        self.lesson_text.setFontPointSize(16)
        self.progress: str = ""
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

    def update_font(self) -> None:
        self.lesson_text.setFontFamily(self.font_box.currentText())
        self.lesson_text.setFontPointSize(self.size_box.value())
        self.lesson_text.update()
        self.update_lesson()

    def process_typing(self) -> None:
        try:
            text: str = self.lesson_text.document().toPlainText()
            new_char: str = self.input_box.text()[-1]
            index: int = len(self.progress)
            next_index: int = len(self.progress) + 1
            # Make sure letter was not removed
            if len(self.progress) > len(self.input_box.text()):
                return
            # Make sure text not overflowed
            if next_index > len(text):
                raise IndexError()
        except IndexError:
            return

        # If text is finished
        if (self.progress + new_char)[: len(text)] == text:
            self.set_underline(index, False)
            self.finished_lesson()
            # TODO: move lesson incrementing to self.finished_lesson()
            self.lesson_box.setValue(self.lesson_box.value() + 1)
        # If correctly typed the character
        elif not text.find(self.progress + new_char):
            self.progress += new_char
            self.set_underline(index, False)
            self.set_underline(next_index)
        # If The character is incorrect
        else:
            self.set_underline(index, fcolor1="red")

    def finished_lesson(self) -> None:  # pylint: disable=no-self-use
        # HACK: remove pylint disable
        # TODO: Add typing stats (Issue #3)
        msg: QMessageBox = QMessageBox()
        msg.setWindowTitle("You finished the lesson.")
        msg.setText("You finished the lesson successfully.")
        msg.setInformativeText("Stats are not available in this version.")
        msg.setStandardButtons(QMessageBox.StandardButton.Close)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def set_underline(
        self,
        i,
        enable=True,
        fcolor1="black",
        bcolor1="yellow",
        fcolor2="green",
        bcolor2="transparent",
    ) -> None:
        try:
            self.cursor.setPosition(i)
            self.cursor.setPosition(i + 1, QTextCursor.MoveMode.KeepAnchor)
        except Exception:
            return
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

    def update_lesson(self) -> None:
        self.input_box.setText("")
        self.progress = ""
        self.load_lesson()

    def load_lesson(self) -> None:
        t: str | None = load_lesson_text(self.lesson_box.text(), self.mode)
        if t is None:
            self.lesson_text.setText(
                "This lesson does not exist. "
                "Please, try another, or add it manually."
            )
            return
        if self.mode.type == "course":
            if len(t) < 5:
                t *= 2
            w = get_ways(list(t))
            if len(w) < 40:
                w = (w * (40 // len(w)))[:41]
            else:
                w = w[:41]
            self.lesson_text.setText(" ".join(["".join(i) for i in w]))
        elif self.mode.type == "words":
            t = t.split("\n")
            w = [random.choice(t) for _ in range(40)]
            self.lesson_text.setText(" ".join(w))
        elif self.mode.type == "random":
            t = "".join([random.choice(t + " ") for _ in range(100)])
            self.lesson_text.setText(t)
        elif self.mode.type == "texts":
            self.lesson_text.setText(t)
        if self.lesson_text.document().toPlainText() != "" and t is not None:
            self.set_underline(0)
        self.input_box.setFocus()
