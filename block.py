from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import event 

class BlockManager:

    def __init__(self):
        self.block_list = BlockList()

    def push(self, widget, pos):
        block = Block(pos)
        self.block_list.push(block)

    def paint(self, widget, canvas):
        for b in self.block_list.list:
            b.paint(widget, canvas)

class BlockList:

    def __init__(self):
        self.list = []

    def push(self, block):
        self.list.append(block)

class Block:

    def __init__(self, pos):
        self.start_x = pos.x()
        self.start_y = pos.y()
        self.end_x = pos.x()
        self.end_y = pos.y()

    def setEndPoint(self, pos):
        self.end_x = pos.x()
        self.end_y = pos.y()

    def paint(self, widget, canvas):
        canvas.setPen(QColor(0, 0, 0))
        canvas.setBrush(QColor(150, 150, 150))
        canvas.drawRect(self.start_x, self.start_y, self.end_x - self.start_x, self.end_y - self.start_y);
