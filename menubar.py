from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

class MenubarManager:

    def __init__(self, widget):
        self.menubar = widget.menuBar()
        self.menubar.setNativeMenuBar(False)

        self.menu_list = []

    def pushAction(self, widget, list_num, image, name, short_cut, descript, func):
        action = Action(widget, image, name, short_cut, descript, func)
        self.menu_list[list_num].addAction(action.action)

    def pushMenu(self, name):
        self.menu_list.append(self.menubar.addMenu(name))

class Action:

    def __init__(self, widget, image, name, short_cut, descript, func):
        self.action = QAction(QIcon(image), name, widget)
        self.action.setShortcut(short_cut)
        self.action.setStatusTip(descript)
        self.action.triggered.connect(func)
