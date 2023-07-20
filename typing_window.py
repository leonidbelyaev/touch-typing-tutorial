import random
import sys
from typing import NoReturn

from PyQt6.QtGui import QBrush, QColor, QFont
from PyQt6.QtGui import QTextCharFormat as QTextCharFmt
from PyQt6.QtGui import QTextCursor
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QMessageBox,
    QTextEdit,
)

from src.design.typing import Ui_Dialog
from src.index import MODE_NAMES
from src.mode import Mode

# enum charcode {
#   NOOP,      00000
#   E,         00001
#   T,         00010
#   N,         00011
#   A,         00100
#   S,         00101
#   H,         00110
#   F,         00111
#   O,         01000
#   R,         01001
#   D,         01010
#   G,         01011
#   L,         01100
#   Y,         01101
#   P,         01110
#   Z,         01111
#   I,         10000
#   C,         10001
#   U,         10010
#   B,         10011
#   M,         10100
#   V,         10101
#   K,         10110
#   COLON,     10111
#   W,         11000
#   J,         11001
#   X,         11010
#   ESCAPE,    11011
#   Q,         11100
#   ENTER,     11101
#   SPACE,     11110
#   BACKSPACE, 11111
# };

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
        with open(filename, encoding="utf-8", mode="r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None


def get_ways(lst: list) -> list:
    ways: list = []
    if len(lst) == 1:
        return lst[0]
    for i in lst:
        ls2: list = lst.copy()
        del ls2[ls2.index(i)]
        for way in get_ways(ls2):
            ways.append([i, *way])
    return ways


class TypingWindow(QDialog, Ui_Dialog):
    def __init__(self, app: QApplication, mode: Mode) -> None:
        super().__init__()
        self.setupUi(self)
        self.app: QApplication = app
        self.mode: Mode = mode
        self.setWindowTitle(f"{MODE_NAMES[mode.type]} — Touch Typing Tutorial")
        self.lesson_text.setFontFamily("Roboto Mono")
        self.lesson_text.setFontPointSize(16)
        self.progress: str = ""
        self.cursor: QTextCursor = self.lesson_text.textCursor()
        self.connect()  # Connections
        # Start Typing
        self.load_lesson()

    def connect(self) -> None:
        # Connections
        self.back_to_menu_btn.clicked.connect(self.close)
        self.quit_btn.clicked.connect(self.exit)
        self.lesson_box.valueChanged.connect(self.update_lesson)
        self.input_box.textChanged.connect(self.process_typing)
        self.apply_btn.clicked.connect(self.update_font)
        self.lesson_text.focusInEvent = lambda e: (
            self.input_box.setFocus()
            and QTextEdit.focusOutEvent(self.lesson_text, e)
        )
        # Set "Apply" button state triggers
        self.font_box.currentTextChanged.connect(
            lambda: self.apply_btn.setEnabled(True)
        )
        self.size_box.valueChanged.connect(
            lambda: self.apply_btn.setEnabled(True)
        )

    def update_font(self) -> None:
        # Ask for confirmation
        msg: QMessageBox = QMessageBox()
        msg.setWindowTitle("Are you sure you want to continue?")
        msg.setText("Are you sure you want to continue?")
        msg.setInformativeText("Some progress might be lost.")
        msg.setStandardButtons(
            QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes
        )
        msg.setDefaultButton(QMessageBox.StandardButton.Yes)
        msg.setIcon(QMessageBox.Icon.Warning)
        if msg.exec() == QMessageBox.StandardButton.Cancel:
            self.font_box.setEditText(self.lesson_text.fontFamily())
            self.size_box.setValue(int(self.lesson_text.fontPointSize()))
        else:
            # Apply the changes
            self.lesson_text.setFontFamily(self.font_box.currentText())
            self.lesson_text.setFontPointSize(self.size_box.value())
            self.lesson_text.setText(self.lesson_text.toPlainText())
            # Recolor all previous letters
            i: int = 0
            for i in range(len(self.progress)):
                self.set_underline(i, False)
            self.set_underline(i + 1)  # Set the current cursor
            self.app.processEvents()
            self.lesson_text.update()
        self.input_box.setFocus()
        self.apply_btn.setEnabled(False)

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
        # If correctly typed the character
        elif not text.find(self.progress + new_char):
            self.progress += new_char
            self.set_underline(index, False)
            self.set_underline(next_index)
        # If The character is incorrect
        else:
            self.set_underline(index, True, True)

    def finished_lesson(self) -> None:
        # TODO: Add typing stats (Issue #3)
        msg: QMessageBox = QMessageBox()
        msg.setWindowTitle("You finished the lesson.")
        msg.setText("You finished the lesson successfully.")
        msg.setInformativeText("Stats are not available in this version.")
        msg.setStandardButtons(
            QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Ok
        )
        msg.setDefaultButton(QMessageBox.StandardButton.Ok)
        msg.setIcon(QMessageBox.Icon.Information)
        if msg.exec() == QMessageBox.StandardButton.Ok:
            self.lesson_box.setValue(self.lesson_box.value() + 1)
        else:
            self.lesson_box.setValue(self.lesson_box.value())

    def set_underline(
        self,
        i,
        enable: bool = True,
        error: bool = False,
        colors: tuple[str, str] = tuple(),
    ) -> None:
        # Handle colors
        if not colors:
            if enable and error:
                colors = ("red", "yellow")
            elif enable:
                colors = ("black", "yellow")
            elif not enable and not error:
                colors = ("green", "transparent")

        # Check if text overflows
        if i > len(self.lesson_text.toPlainText()):
            return

        self.cursor.setPosition(i)
        self.cursor.movePosition(
            QTextCursor.MoveOperation.NextCharacter,
            QTextCursor.MoveMode.KeepAnchor,
        )

        fmt: QTextCharFmt = self.cursor.charFormat()

        # Set colors
        fmt.setForeground(QBrush(QColor(colors[0])))
        fmt.setBackground(QBrush(QColor(colors[1])))

        # Other styling
        if enable:
            fmt.setUnderlineStyle(QTextCharFmt.UnderlineStyle.SingleUnderline)
            fmt.setFontWeight(QFont.Weight.Bold)
        else:
            fmt.setUnderlineStyle(QTextCharFmt.UnderlineStyle.NoUnderline)
            fmt.setFontWeight(QFont.Weight.Normal)

        # Apply
        self.cursor.setCharFormat(fmt)

    def exit(self) -> NoReturn:
        self.hide()
        sys.exit(0)

    def update_lesson(self) -> None:
        self.input_box.setText("")
        self.progress = ""
        self.load_lesson()

    def load_lesson(self) -> None:
        apply = self.lesson_text.setText  # setText() alias
        mode: Mode = self.mode
        lesson: str | None = load_lesson_text(self.lesson_box.text(), mode)
        if lesson is None:
            self.lesson_text.setText(
                "This lesson does not exist. "
                "Please, try another, or add it manually."
            )
            return
        if mode.type == "course":
            lesson *= 2 if len(lesson) < 5 else 1  # Make sure not too short
            if len(lesson) > 7:
                lst: list[str] = [
                    "".join(random.sample(lesson, 6)) for _ in range(40)
                ]
            else:
                lst: list[str] = get_ways(list(lesson))
                random.shuffle(lst)
            if len(lst) < 40:
                lst: list[str] = (lst * (40 // len(lst)))[:41]
            else:
                lst: list[str] = lst[:41]
            apply(" ".join(["".join(i) for i in lst]))
        elif mode.type == "words":
            lst: list[str] = [
                random.choice(lesson.splitlines()) for _ in range(40)
            ]
            apply(" ".join(lst))
        elif mode.type == "random":
            apply("".join([random.choice(lesson + " ") for _ in range(100)]))
        elif mode.type == "texts":
            apply(lesson)
        if (
            self.lesson_text.document().toPlainText() != ""
            and lesson is not None
        ):
            self.set_underline(0)
        self.input_box.setFocus()
