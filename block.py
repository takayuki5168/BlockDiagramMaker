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

        self.mode = 0 # -1:死 0:選択途中 1:選択終了 

        self.near_obj_pos_dis = [] # Blockの二辺とあるオブジェクトとその最短位置、距離
        self.selected_obj = -1 # Blockが選択しているオブジェクト

    def setEndPoint(self, pos):
        self.end_pos = pos

    def showFormula(self, widget):
        self.nume, ok = QInputDialog.getText(widget, 'Input Diagram', 'Input Numerator(分母):')
        self.deno, ok = QInputDialog.getText(widget, 'Input Diagram', 'Input Denominator(分子):')
        while self.deno == '':
            self.deno, ok = QInputDialog.getText(widget, 'Input Diagram', 'Input Denominator(分子):')


        if self.nume == '':
            self.label_deno = QLabel(self.deno, widget)
            self.label_deno.move(self.start_pos.x(), self.start_pos.y())
        else:
            self.label_nume = QLabel(self.nume, widget)
            self.label_deno = QLabel(self.deno, widget)
            self.label_nume.move(self.start_pos.x(),  0.5 * self.start_pos.y() + 0.5 * self.end_pos.y())
            self.label_deno.move(self.start_pos.x(), self.start_pos.y())

#    def nearObjPosDis(self, mouse_pos, all_obj):
#
#        for o in all_obj:
#            # まずは全部青でなくする
#            o.setFrameBlue(False)
#        if min_dis < 6: # 距離が十分近かったら
#            # そのオブジェクトを青にして選択する
#            min_obj.setFrameBlue(True)
#            self.setEndPoint(min_pos)
#        else:
#            self.near_obj_pos_dis = []
#            self.setEndPoint(mouse_pos)
#
    def paint(self, widget, canvas):
        if self.mode == -1:
            return

        if self.frame_blue == False:
            canvas.setPen(QColor(0, 0, 0))
        else:
            canvas.setPen(QColor(0, 0, 255))
        canvas.setBrush(QColor(200, 200, 200))
        canvas.drawRect(self.start_pos.x(), self.start_pos.y(), self.end_pos.x() - self.start_pos.x(), self.end_pos.y() - self.start_pos.y());

        # 伝達関数の表示
        if self.label_nume != None:
            self.label_nume.show()
            canvas.drawLine(self.start_pos.x() + 5, 0.5 * self.start_pos.y() + 0.5 * self.end_pos.y(),
                    self.end_pos.x() - 5, 0.5 * self.start_pos.y() + 0.5 * self.end_pos.y())
        if self.label_deno != None:
            self.label_deno.show()

    def setFrameBlue(self, blue_or_not):
        if blue_or_not:
            self.frame_blue = True
        else:
            self.frame_blue = False
