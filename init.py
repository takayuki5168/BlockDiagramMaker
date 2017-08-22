#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import qApp
from PyQt5.QtCore import QTimer

import menubar, button, event, block, arrow, combine, simulate, analysis

def init(window):
    initUI(window)
    initTimer(window)
    initEvent(window)

    window.setMouseTracking(True)
    window.operate_mode = 'None'

def initUI(window):
    initMenubar(window)
    initButton(window)
    initBlock(window)
    initArrow(window)
    initCombine(window)
    initSimulate(window)
    initAnalysis(window)

    window.setGeometry(300, 300, 640, 480)
    window.setWindowTitle('BlockDiagramMaker')

def initMenubar(window):
    window.menu_manager = menubar.MenubarManager(window)

    window.menu_manager.pushMenu('&File')
    window.menu_manager.pushAction(window, 0, 'po.png', '&Exit', 'Ctrl+Q', 'Exit application', qApp.quit)

def initButton(window):
    window.button_manager = button.ButtonManager()

    name = ['Cursor', 'Block', 'Arrow', 'Combine', 'Simulate', 'Clear', 'Exit']
    for i in range(len(name)):
        window.button_manager.push(name[i], window, 10 + i * 65, 30, window.setOperateMode)

def initBlock(window):
    window.block_manager = block.BlockManager()

def initArrow(window):
    window.arrow_manager = arrow.ArrowManager()

def initCombine(window):
    window.combine_manager = combine.CombineManager()

def initSimulate(window):
    window.simulate = simulate.Simulate()

def initAnalysis(window):
    window.analysis = analysis.Analysis()

def initTimer(window):
    window.timer = QTimer(window)
    window.timer.timeout.connect(window.update)
    window.timer.start(10) # 10ms間隔で更新

def initEvent(window):
    window.event = event.Event()
