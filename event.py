from PyQt5.QtWidgets import * #QWidget, QPushButton, QFrame, QApplication, QLineEdit
from PyQt5.QtGui import *

import block

class Event:
    def __init__(self):
        self.block_id = -1
        self.arrow_id = 0

    def mousePress(self, mouse_event, widget):
        pos = mouse_event.pos()

        if widget.mode == 'Block':
            self.block_id = len(widget.block_manager.block_list.list)
            widget.block_manager.push(widget, pos)
        elif widget.mode == 'Arrow':
            #self.arrow_id = len(widget.arrow_manager.arrow_list.list)
            widget.arrow_manager.push(widget)
            widget.arrow_manager.arrow_list.list[self.arrow_id].setWayPoint(pos)

    def mouseMove(self, mouse_event, widget):
        pos = mouse_event.pos()

        if widget.mode == 'Block':
            if self.block_id != -1:
                widget.block_manager.block_list.list[self.block_id].setEndPoint(pos)

    def mouseRelease(self, mouse_event, widget):
        pos = mouse_event.pos()

        if widget.mode == 'Block':
            self.block_id = -1
