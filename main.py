#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import signal

from PyQt5.QtWidgets import * #QWidget, QPushButton, QFrame, QApplication, QLineEdit
from PyQt5.QtGui import *

import init, event, button, block, arrow

class MyWidget(QWidget):

    def __init__(self):
        super().__init__()
        signal.signal(signal.SIGINT, self.sigIntHandler)
        init.init(self)
        self.setMouseTracking(True)
        self.mode = 'None'

        self.show()

    def mousePressEvent(self, mouse_event):
        self.event.mousePress(mouse_event, self)

    def mouseMoveEvent(self, mouse_event):
        self.event.mouseMove(mouse_event, self)

    def mouseReleaseEvent(self, mouse_event):
        self.event.mouseRelease(mouse_event, self)

    def keyPressEvent(self, key_event):
        self.event.keyPress(key_event, self)

    def paintEvent(self, event):
        canvas = QPainter(self)

        self.block_manager.paint(self, canvas)
        self.arrow_manager.paint(self, canvas)

    def setMode(self, toggled):
        source = self.sender()

        if toggled:
            self.button_manager.setButton(source.text())
            self.mode = source.text()

    def sigIntHandler(self, signal, frame):
        print('call SigIntHandler')
        sys.exit(0)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    my_widget = MyWidget()
    sys.exit(app.exec_())
