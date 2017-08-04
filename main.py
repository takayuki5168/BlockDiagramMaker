#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import * #QWidget, QPushButton, QFrame, QApplication, QLineEdit
from PyQt5.QtGui import *

import button, block

class MyWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.cursor_button = QPushButton('Cursor', self)
        self.cursor_button.setCheckable(True)
        self.cursor_button.move(10, 10)
        self.cursor_button.clicked[bool].connect(self.setMode)

        self.block_button = QPushButton('Block', self)
        self.block_button.setCheckable(True)
        self.block_button.move(100, 10)
        self.block_button.clicked[bool].connect(self.setMode)

        self.arrow_button = QPushButton('Arrow', self)
        self.arrow_button.setCheckable(True)
        self.arrow_button.move(190, 10)
        self.arrow_button.clicked[bool].connect(self.setMode)

        self.remove_button = QPushButton('Remove', self)
        self.remove_button.setCheckable(True)
        self.remove_button.move(280, 10)
        self.remove_button.clicked[bool].connect(self.setMode)

        self.undo_button = QPushButton('Undo', self)
        self.undo_button.setCheckable(True)
        self.undo_button.move(370, 10)
        self.undo_button.clicked[bool].connect(self.setMode)

        self.save_button = QPushButton('Save', self)
        self.save_button.setCheckable(True)
        self.save_button.move(460, 10)
        self.save_button.clicked[bool].connect(self.setMode)

        self.buttons = [self.cursor_button, self.block_button, self.arrow_button,
                self.remove_button, self.undo_button, self.save_button]

        self.textbox = QLineEdit(self)
        self.textbox.move(100,100)
        self.textbox.resize(140,20)
        self.textbox.resize(180,20)
        self.textbox.resize(200,20)


        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle('BlockDiagramMaker')
        self.show()

    def paintEvent(self, event):
        blocks = block.ExtendedBlock(self, 100, 100)

    def mousePressEvent(self, event):
        event.pos

    def setMode(self, pressed):
        # 押されたボタンはどれか
        source = self.sender()

        if pressed:
            self.setButtonAllFalse()
            if source.text() == 'Cursor':
                self.mode = 'cursor_mode'
                self.cursor_button.setChecked(True)
            elif source.text() == 'Block':
                self.mode = 'block_mode'
                self.block_button.setChecked(True)
            elif source.text() == 'Arrow':
                self.mode = 'arrow_mode'
                self.arrow_button.setChecked(True)
            elif source.text() == 'Remove':
                self.mode = 'remove_mode'
                self.remove_button.setChecked(True)
            elif source.text() == 'Undo':
                self.mode = 'undo_mode'
                self.undo_button.setChecked(True)
            elif source.text() == 'Save':
                self.mode = 'save_mode'
                self.save_button.setChecked(True)

    def setButtonAllFalse(self):
        for b in self.buttons:
            b.setChecked(False)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    my_widget = MyWidget()
    sys.exit(app.exec_())
