from PyQt5.QtWidgets import * #QWidget, QPushButton, QFrame, QApplication, QLineEdit
from PyQt5.QtGui import *

import button

def initUI(widget):
    initButton(widget)

    textbox = QLineEdit()
    textbox.move(100,100)
    textbox.resize(140,20)
    textbox.resize(180,20)
    textbox.resize(200,20)

    widget.setGeometry(300, 300, 640, 480)
    widget.setWindowTitle('BlockDiagramMaker')

def initButton(widget):
    widget.button_manager = button.ButtonManager()

    widget.cursor_button = widget.button_manager.push('Cursor', widget, 10, 10, widget.setMode)
    widget.block_button = widget.button_manager.push('Block', widget, 100, 10, widget.setMode)
    widget.arrow_button = widget.button_manager.push('Arrow', widget, 190, 10, widget.setMode)
    widget.remove_button = widget.button_manager.push('Remove', widget, 280, 10, widget.setMode)
    widget.undo_button = widget.button_manager.push('Undo', widget, 370, 10, widget.setMode)
    widget.save_button = widget.button_manager.push('Save', widget, 460, 10, widget.setMode)
