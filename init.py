from PyQt5.QtWidgets import * #QWidget, QPushButton, QFrame, QApplication, QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer

import menubar, button, event, block, arrow, combine

def init(widget):
    initUI(widget)
    initTimer(widget)
    initEvent(widget)

def initUI(widget):
    initMenubar(widget)
    initButton(widget)
    initBlock(widget)
    initArrow(widget)
    initCombine(widget)

    widget.setGeometry(300, 300, 640, 480)
    widget.setWindowTitle('BlockDiagramMaker')

def initMenubar(widget):
    widget.menu_manager = menubar.MenubarManager(widget)

    widget.menu_manager.pushMenu('&File')
    widget.menu_manager.pushAction(widget, 0, 'po.png', '&Exit', 'Ctrl+Q', 'Exit application', qApp.quit)

def initButton(widget):
    widget.button_manager = button.ButtonManager()

    name = ['Cursor', 'Block', 'Arrow', 'Combine', 'Undo', 'Save', 'Exit']
    for i in range(len(name)):
        widget.button_manager.push(name[i], widget, 10 + i * 65, 30, widget.setOperateMode)

def initBlock(widget):
    widget.block_manager = block.BlockManager()

def initArrow(widget):
    widget.arrow_manager = arrow.ArrowManager()

def initCombine(widget):
    widget.combine_manager = combine.CombineManager()

def initTimer(widget):
    widget.timer = QTimer(widget)
    widget.timer.timeout.connect(widget.update)
    widget.timer.start(10) # 10ms間隔で更新

def initEvent(widget):
    widget.event = event.Event()

