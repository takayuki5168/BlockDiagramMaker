from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import event 

class ArrowManager:

    def __init__(self):
        self.arrow_list = ArrowList()

    def push(self, widget):
        arrow = Arrow()
        self.arrow_list.push(arrow)

    def paint(self, widget, canvas):
        for a in self.arrow_list.list:
            a.paint(widget, canvas)

class ArrowList:

    def __init__(self):
        self.list = []

    def push(self, arrow):
        self.list.append(arrow)

class Arrow:

    def __init__(self):
        self.pos = []

    def setWayPoint(self, pos):
        self.pos.append(pos)
        print(len(self.pos))

    def paint(self, widget, canvas):
        canvas.setPen(QColor(0, 0, 0))
        canvas.setBrush(QColor(150, 150, 150))
        for i in range(len(self.pos) - 1):
            canvas.drawLine(self.pos[i], self.pos[i + 1])
