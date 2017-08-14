#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import event

class BlockManager:

    def __init__(self):
        self.block_list = [] # list of managing Block

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

        self.mode = 0 # -1:死 0:選択開始(選択途中) 1:選択途中

        self.near_obj_pos_dis = [] # Blockの二辺とあるオブジェクトとその最短位置、距離
        self.selected_obj = -1 # Blockが選択しているオブジェクト

        self.input = []
        self.output = []

    def setEndPoint(self, pos):
        self.end_pos = pos

    def showFormula(self, widget):
        self.nume, is_ok = QInputDialog.getText(widget, 'Input Diagram', 'Input Numerator(分母):')
        if is_ok == False:
            self.mode = -1
            return
        self.deno, is_ok = QInputDialog.getText(widget, 'Input Diagram', 'Input Denominator(分子):')
        if is_ok == False:
            self.mode = -1
            return

        while self.deno == '':
            self.deno, is_ok = QInputDialog.getText(widget, 'Input Diagram', 'Input Denominator(分子):')
            if is_ok == False:
                self.mode = -1
                return

        font = QFont()
        font.setPointSize(20)


        if self.nume == '':
            self.label_deno = QLabel(self.deno, widget)

            deno_width = self.label_deno.fontMetrics().boundingRect(self.label_deno.text()).width()
            deno_height = self.label_deno.fontMetrics().boundingRect(self.label_deno.text()).height()

            self.label_deno.move((self.start_pos.x() + self.end_pos.x()) / 2.0 - deno_width,
                    (self.start_pos.y() + self.end_pos.y()) / 2.0 - deno_height / 2.0)
            self.label_deno.setFixedWidth(deno_width * 2)
            self.label_deno.setFont(font)
            #print(deno_width)
            #print(deno_height)
        else:
            self.label_nume = QLabel(self.nume, widget)
            self.label_deno = QLabel(self.deno, widget)

            nume_width = self.label_nume.fontMetrics().boundingRect(self.label_nume.text()).width()
            nume_height = self.label_nume.fontMetrics().boundingRect(self.label_nume.text()).height()
            deno_width = self.label_deno.fontMetrics().boundingRect(self.label_deno.text()).width()
            deno_height = self.label_deno.fontMetrics().boundingRect(self.label_deno.text()).height()

            self.label_nume.move((self.start_pos.x() + self.end_pos.x()) / 2.0 - nume_width,
                    (self.start_pos.y() + self.end_pos.y()) / 2.0)
            self.label_deno.move((self.start_pos.x() + self.end_pos.x()) / 2.0 - deno_width,
                    (self.start_pos.y() + self.end_pos.y()) / 2.0 - deno_height - 20)

            self.label_nume.setFixedWidth(nume_width * 2)
            self.label_deno.setFixedWidth(deno_width * 2)

            self.label_nume.setFont(font)
            self.label_deno.setFont(font)

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
            canvas.setPen(QPen(QColor(0, 0, 0), 2))
        else:
            canvas.setPen(QPen(QColor(0, 0, 255), 2))
        canvas.setBrush(QColor(200, 200, 200))
        canvas.drawRect(self.start_pos.x(), self.start_pos.y(), self.end_pos.x() - self.start_pos.x(), self.end_pos.y() - self.start_pos.y());

        # 伝達関数の表示
        if self.label_nume != None:
            self.label_nume.show()
            canvas.setPen(QPen(QColor(0, 0, 0), 2))
            canvas.drawLine(self.start_pos.x() + 10, (self.start_pos.y() + self.end_pos.y()) / 2.0,
                    self.end_pos.x() - 10, (self.start_pos.y() + self.end_pos.y()) / 2.0)
        if self.label_deno != None:
            self.label_deno.show()

    def setFrameBlue(self, blue_or_not):
        if blue_or_not:
            self.frame_blue = True
        else:
            self.frame_blue = False
