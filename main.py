#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import * #QWidget, QPushButton, QFrame, QApplication, QLineEdit
from PyQt5.QtGui import *

import init, button, block

class MyWidget(QWidget):

    def __init__(self):
        super().__init__()

        init.initUI(self)

        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle('BlockDiagramMaker')
        self.show()

    def paintEvent(self, event):
        blocks = block.ExtendedBlock(self, 100, 100)

    def mousePressEvent(self, event):
        event.pos

    def setMode(self, toggled):
        source = self.sender()

        if toggled:
            self.button_manager.setButton(source.text())
            self.mode = source.text()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    my_widget = MyWidget()
    sys.exit(app.exec_())
