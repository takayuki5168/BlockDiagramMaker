#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import event

class BlockManager:

    def __init__(self):
        self.block_list = [] # Blockを管理するリスト

    def push(self, widget, pos):
        block = Block(pos)
        self.block_list.append(block)


    def paint(self, widget, canvas):
        for b in self.block_list:
            b.paint(widget, canvas)

class Block:

    def __init__(self, pos):
        self.start_pos = pos
        self.end_pos = pos

        self.frame_blue = False # 枠を青くするかどうか

        self.label_nume = None # 分母の式ラベル
        self.label_deno = None # 分子の式ラベル

    def setEndPoint(self, widget, pos):
        self.end_x = pos.x()
        self.end_y = pos.y()

    def showFormula(self, widget):
        self.nume, ok = QInputDialog.getText(widget, 'Input Diagram', 'Input Numerator(分母):')
        self.deno, ok = QInputDialog.getText(widget, 'Input Diagram', 'Input Denominator(分子):')

        if self.nume == '':
            self.lb_deno = QLabel(self.deno, widget)
            self.lb_deno.move(self.start_x, self.start_y)
        else:
            self.lb_nume = QLabel(self.nume, widget)
            self.lb_deno = QLabel(self.deno, widget)
            self.lb_nume.move(self.start_x,  0.5 * self.start_y + 0.5 * self.end_y)
            self.lb_deno.move(self.start_x, self.start_y)



    def paint(self, widget, canvas):
        if not self.is_alive:
            return

        if self.frame_blue == False:
            canvas.setPen(QColor(0, 0, 0))
        else:
            canvas.setPen(QColor(0, 0, 255))
        canvas.setBrush(QColor(200, 200, 200))
        canvas.drawRect(self.start_x, self.start_y, self.end_x - self.start_x, self.end_y - self.start_y);

        # 伝達関数の表示
        if self.lb_nume != None:
            self.lb_nume.show()
            canvas.drawLine(self.start_x + 5, 0.5 * self.start_y + 0.5 * self.end_y,
                    self.end_x - 5, 0.5 * self.start_y + 0.5 * self.end_y)
        if self.lb_deno != None:
            self.lb_deno.show()


    def setFrameBlue(self, blue_or_not):
        if blue_or_not:
            self.frame_blue = True
        else:
            self.frame_blue = False
