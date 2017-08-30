#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import qApp
from PyQt5.QtCore import QTimer

import menubar, button, event, block, arrow, combine, simulate, analysis, identificate

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
    initIdentificate(w)

    w.setGeometry(200, 0, 960, 720)
    w.setWindowTitle('BlockDiagramMaker')

def initMenubar(w):
    w.menu_manager = menubar.MenubarManager(w)

    w.menu_manager.pushMenu('&File')
    w.menu_manager.pushAction(w, 0, 'po.png', '&Exit', 'Ctrl+Q', 'Exit application', qApp.quit)

    w.menu_manager.pushMenu('&Tool')
    w.menu_manager.pushAction(w, 1, 'po.png', '&System Identification', 'Ctrl+Q', 'System Identification', lambda : w.identificate.execute(w))

def initButton(w):
    w.button_manager = button.ButtonManager()

    name = ['Cursor', 'Block', 'Arrow', 'Combine', 'Input', 'Scope', 'Simulate', 'Clear', 'Exit']
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

def initIdentificate(w):
    w.identificate = identificate.Identificate()

def initTimer(w):
    w.timer = QTimer(w)
    w.timer.timeout.connect(w.update)
    w.timer.start(10) # 10ms間隔で更新

def initEvent(w):
    w.event = event.Event()
