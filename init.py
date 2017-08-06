from PyQt5.QtWidgets import * #QWidget, QPushButton, QFrame, QApplication, QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer

import button, event, block, arrow

def init(widget):
    initUI(widget)
    initTimer(widget)
    initEvent(widget)

def initUI(widget):
    initButton(widget)
    initBlock(widget)
    initArrow(widget)

    #textbox = QLineEdit()
    #textbox.move(100,100)
    #textbox.resize(140,20)
    #textbox.resize(180,20)
    #textbox.resize(200,20)

    widget.setGeometry(300, 300, 640, 480)
    widget.setWindowTitle('BlockDiagramMaker')

def initButton(widget):
    widget.button_manager = button.ButtonManager()

    widget.button_manager.push('Cursor', widget, 10, 10, widget.setMode)
    widget.button_manager.push('Block', widget, 100, 10, widget.setMode)
    widget.button_manager.push('Arrow', widget, 190, 10, widget.setMode)
    widget.button_manager.push('Remove', widget, 280, 10, widget.setMode)
    widget.button_manager.push('Undo', widget, 370, 10, widget.setMode)
    widget.button_manager.push('Save', widget, 460, 10, widget.setMode)
    widget.button_manager.push('Exit', widget, 550, 10, widget.close)

    #widget.button_manager.button_list.list[0].button.setChecked(True)

def initBlock(widget):
    widget.block_manager = block.BlockManager()

def initArrow(widget):
    widget.arrow_manager = arrow.ArrowManager()

def initTimer(widget):
    widget.timer = QTimer(widget)
    widget.timer.timeout.connect(widget.update)
    widget.timer.start(10)#一秒間隔で更新

def initEvent(widget):
    widget.event = event.Event()

