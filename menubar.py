from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

class MenubarManager:

    def __init__(self, window):
        self.menubar = window.menuBar()
        self.menubar.setNativeMenuBar(False)

        self.menu_list = []

    def pushAction(self, window, list_num, image, name, short_cut, descript, func):
        action = Action(window, image, name, short_cut, descript, func)
        self.menu_list[list_num].addAction(action.action)

    def pushMenu(self, name):
        self.menu_list.append(self.menubar.addMenu(name))

class Action:

    def __init__(self, window, image, name, short_cut, descript, func):
        self.action = QAction(QIcon(image), name, window)
        self.action.setShortcut(short_cut)
        self.action.setStatusTip(descript)
        self.action.triggered.connect(func)
