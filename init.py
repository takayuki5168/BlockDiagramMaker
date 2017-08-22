#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import qApp
from PyQt5.QtCore import QTimer

import menubar, button, event, block, arrow, combine, simulate, analysis

def init(w):
    initUI(w)
    initTimer(w)
    initEvent(w)

    w.setMouseTracking(True)
    w.operate_mode = 'None'

def initUI(w):
    initMenubar(w)
    initButton(w)
    initBlock(w)
    initArrow(w)
    initCombine(w)
    initSimulate(w)
    initAnalysis(w)

    w.setGeometry(300, 300, 640, 480)
    w.setWindowTitle('BlockDiagramMaker')

def initMenubar(w):
    w.menu_manager = menubar.MenubarManager(w)

    w.menu_manager.pushMenu('&File')
    w.menu_manager.pushAction(w, 0, 'po.png', '&Exit', 'Ctrl+Q', 'Exit application', qApp.quit)

def initButton(w):
    w.button_manager = button.ButtonManager()

    name = ['Cursor', 'Block', 'Arrow', 'Combine', 'Simulate', 'Clear', 'Exit']
    for i in range(len(name)):
        w.button_manager.push(name[i], w, 10 + i * 65, 30, w.setOperateMode)

def initBlock(w):
    w.block_manager = block.BlockManager()

def initArrow(w):
    w.arrow_manager = arrow.ArrowManager()

def initCombine(w):
    w.combine_manager = combine.CombineManager()

def initSimulate(w):
    w.simulate = simulate.Simulate()

def initAnalysis(w):
    w.analysis = analysis.Analysis()

def initTimer(w):
    w.timer = QTimer(w)
    w.timer.timeout.connect(w.update)
    w.timer.start(10) # 10ms間隔で更新

def initEvent(w):
    w.event = event.Event()
