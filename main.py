#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import signal

from PyQt5.QtWidgets import QMainWindow, QPushButton, QFrame, QApplication, QLineEdit
from PyQt5.QtGui import QPainter

import init, event, button, block, arrow

class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        init.init(self)

        signal.signal(signal.SIGINT, self.sigIntHandler)

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
        self.combine_manager.paint(self, canvas)

    def setOperateMode(self, toggled):
        source = self.sender()

        if toggled:
            self.button_manager.setButton(source.text())
            self.operate_mode = source.text()

            if self.operate_mode == 'Simulate':
                print('Simulate')
                self.simulate.initArrowFunc(self)
                self.simulate.updateArrowFunc(self)
            elif self.operate_mode == 'Clear':
                for b in self.block_manager.block_list:
                    b.mode = -1
                for a in self.arrow_manager.arrow_list:
                    a.mode = -1
                for c in self.combine_manager.combine_list:
                    c.mode = -1

    def sigIntHandler(self, signal, frame):
        print('call SigIntHandler')
        sys.exit(0)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    my_window = MyWindow()
    sys.exit(app.exec_())
