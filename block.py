from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class ExtendedBlock: 

    def __init__(self, widget, x, y):
        self.box = QPainter(widget)
        self.box.setPen(QColor(0, 0, 20))
        self.box.setBrush(QColor(1, 20, 0))
        self.start_x = x
        self.start_y = y
        self.box.drawRect(self.start_x, self.start_y, self.start_x + 10, self.start_y + 10);
