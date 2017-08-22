from PyQt5.QtWidgets import QPushButton, QFrame, QApplication, QLineEdit
from PyQt5.QtGui import QColor

class ButtonManager:

    def __init__(self):
        self.button_list = []

    def push(self, name, w, x, y, func):
        button = ToggleButton(name, w, x, y, func)
        self.button_list.append(button)

    def setButton(self, text):
        for b in self.button_list:
            if b.button.text() == text:
                b.button.setChecked(True)
            else:
                b.button.setChecked(False)

class ToggleButton:

    def __init__(self, name, w, x, y, func):
        self.button = QPushButton(name, w)
        self.button.setCheckable(True)
        self.button.move(x, y)
        self.button.clicked[bool].connect(func)
        self.button.resize(65, 30)
