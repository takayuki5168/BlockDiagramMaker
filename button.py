from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QApplication, QLineEdit
from PyQt5.QtGui import QColor

class ExtendedToggleButton:
    def __init__(self, name, widget, x, y, func):
        self.button = QPushButton(name, widget)
        self.button.setCheckable(True)
        self.button.move(x, y)
        self.button.clicked[bool].connect(func)
