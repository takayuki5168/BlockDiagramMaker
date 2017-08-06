from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import event 

class BlockManager:

    def __init__(self):
        self.block_list = []

    def push(self, widget, pos):
        block = Block(pos)
        self.block_list.append(block)

    def paint(self, widget, canvas):
        for b in self.block_list:
            b.paint(widget, canvas)

class Block:

    def __init__(self, pos):
        self.start_x = pos.x()
        self.start_y = pos.y()
        self.end_x = pos.x()
        self.end_y = pos.y()

        self.frame_blue = False # カーソルの選択範囲に入っているか

    def setEndPoint(self, pos):
        self.end_x = pos.x()
        self.end_y = pos.y()

    def paint(self, widget, canvas):
        if self.frame_blue == False:
            canvas.setPen(QColor(0, 0, 0))
        else:
            canvas.setPen(QColor(0, 0, 255))
        canvas.setBrush(QColor(200, 200, 200))
        canvas.drawRect(self.start_x, self.start_y, self.end_x - self.start_x, self.end_y - self.start_y);
    def setFrameBlue(self, blue_or_not):
        if blue_or_not:
            self.frame_blue = True
        else:
            self.frame_blue = False
