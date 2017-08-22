#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

class MenubarManager:

    def __init__(self, w):
        self.menubar = w.menuBar()
        self.menubar.setNativeMenuBar(False)

        self.menu_list = []

    def pushAction(self, w, list_num, image, name, short_cut, descript, func):
        action = Action(w, image, name, short_cut, descript, func)
        self.menu_list[list_num].addAction(action.action)

    def pushMenu(self, name):
        self.menu_list.append(self.menubar.addMenu(name))

class Action:

    def __init__(self, w, image, name, short_cut, descript, func):
        self.action = QAction(QIcon(image), name, w)
        self.action.setShortcut(short_cut)
        self.action.setStatusTip(descript)
        self.action.triggered.connect(func)
