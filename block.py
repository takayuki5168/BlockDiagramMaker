#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QInputDialog, QLabel, QAction, QMenu
from PyQt5.QtGui import QPen, QColor, QFont

import event

class BlockManager:

    def __init__(self):
        self.block_list = [] # list of managing Block

    def push(self, window, pos):
        block = Block(pos)
        self.block_list.append(block)

    def paint(self, window, canvas):
        for b in self.block_list:
            b.paint(window, canvas)

    def whichBlue(self):
        for b in self.block_list:
            if b.is_blue:
                return self.block_list.index(b)
        return -1

class Block:

    def __init__(self, pos):
        self.start_pos = pos
        self.end_pos = pos

        self.is_blue = False # 枠を青くするかどうか

        self.label_deno = None # 分母の式ラベル
        self.label_nume = None # 分子の式ラベル

        self.mode = 0 # -1:死 0:選択開始(選択途中) 1:選択途中

        self.near_obj_pos_dis = [] # Blockの二辺とあるオブジェクトとその最短位置、距離
        self.selected_obj = -1 # Blockが選択しているオブジェクト

        self.input = []
        self.output = []

    def setEndPoint(self, pos):
        self.end_pos = pos

    def showFormula(self, window):
        # 分母を入力
        self.deno_coef, is_ok = QInputDialog.getText(window, 'Input Diagram', 'Input denorator(分母):')
        if is_ok == False:
            self.mode = -1
            return
        self.deno_coef = self.deno_coef.split(' ')
        while '' in self.deno_coef:
            self.deno_coef.remove('')
        self.deno = ''
        for i in range(len(self.deno_coef)):
            if i == len(self.deno_coef) - 1:
                self.deno += self.deno_coef[i]
            elif i == len(self.deno_coef) - 2:
                self.deno += self.deno_coef[i] + 's + '
            else:
                self.deno += self.deno_coef[i] + 's^' + str(len(self.deno_coef) - 1 - i) + ' + '

        # 分子を入力
        self.nume_coef, is_ok = QInputDialog.getText(window, 'Input Diagram', 'Input numeminator(分子):')
        if is_ok == False:
            self.mode = -1
            return
        self.nume_coef = self.nume_coef.split(' ')
        while '' in self.nume_coef:
            self.nume_coef.remove('')
        self.nume = ''
        for i in range(len(self.nume_coef)):
            if i == len(self.nume_coef) - 1:
                self.nume += self.nume_coef[i]
            elif i == len(self.nume_coef) - 2:
                self.nume += self.nume_coef[i] + 's + '
            else:
                self.nume += self.nume_coef[i] + 's^' + str(len(self.nume_coef) - 1 - i) + ' + '

        while self.nume == '':
            self.nume, is_ok = QInputDialog.getText(window, 'Input Diagram', 'Input numeminator(分子):')
            if is_ok == False:
                self.mode = -1
                return

        font = QFont()
        font.setPointSize(20)

        if self.deno == '': # 分母のみのとき
            self.label_nume = QLabel(self.nume, window)

            nume_width = self.label_nume.fontMetrics().boundingRect(self.label_nume.text()).width()
            nume_height = self.label_nume.fontMetrics().boundingRect(self.label_nume.text()).height()

            self.label_nume.move((self.start_pos.x() + self.end_pos.x()) / 2.0 - nume_width,
                    (self.start_pos.y() + self.end_pos.y()) / 2.0 - nume_height / 2.0)
            self.label_nume.setFixedWidth(nume_width * 2)
            self.label_nume.setFont(font)
            #print(nume_width)
            #print(nume_height)
        else: # 分母もあるとき
            self.label_deno = QLabel(self.deno, window)
            self.label_nume = QLabel(self.nume, window)

            deno_width = self.label_deno.fontMetrics().boundingRect(self.label_deno.text()).width()
            deno_height = self.label_deno.fontMetrics().boundingRect(self.label_deno.text()).height()
            nume_width = self.label_nume.fontMetrics().boundingRect(self.label_nume.text()).width()
            nume_height = self.label_nume.fontMetrics().boundingRect(self.label_nume.text()).height()

            self.label_deno.move((self.start_pos.x() + self.end_pos.x()) / 2.0 - deno_width,
                    (self.start_pos.y() + self.end_pos.y()) / 2.0)
            self.label_nume.move((self.start_pos.x() + self.end_pos.x()) / 2.0 - nume_width,
                    (self.start_pos.y() + self.end_pos.y()) / 2.0 - nume_height - 20)

            self.label_deno.setFixedWidth(deno_width * 2)
            self.label_nume.setFixedWidth(nume_width * 2)

            self.label_deno.setFont(font)
            self.label_nume.setFont(font)

    def paint(self, window, canvas):
        if self.mode == -1:
            if type(self.label_deno) != type(None):
                self.label_deno.clear()
            if type(self.label_nume) != type(None):
                self.label_nume.clear()
            return

        if self.is_blue == False:
            canvas.setPen(QPen(QColor(0, 0, 0), 2))
        else:
            canvas.setPen(QPen(QColor(0, 0, 255), 2))
        canvas.setBrush(QColor(200, 200, 200))
        canvas.drawRect(self.start_pos.x(), self.start_pos.y(), self.end_pos.x() - self.start_pos.x(), self.end_pos.y() - self.start_pos.y());

        # 伝達関数の表示
        if self.label_deno != None:
            self.label_deno.show()
            canvas.setPen(QPen(QColor(0, 0, 0), 2))
            canvas.drawLine(self.start_pos.x() + 10, (self.start_pos.y() + self.end_pos.y()) / 2.0,
                    self.end_pos.x() - 10, (self.start_pos.y() + self.end_pos.y()) / 2.0)
        if self.label_nume != None:
            self.label_nume.show()

    def setFrameBlue(self, blue_or_not):
        if blue_or_not:
            self.is_blue = True
        else:
            self.is_blue = False

    def onRightClick(self, pos, window):
        menu = QMenu(window)
        action = [(QAction('Analysis Bode', window, triggered = lambda : window.analysis.analysis(window, self, 'bode'))),
                QAction('Analysis RootLocus', window, triggered = lambda : window.analysis.analysis(window, self, 'rlocus')),
                QAction('Analysis Step Response', window, triggered = lambda : window.analysis.analysis(window, self, 'step')),
                QAction('Analysis Impulse Response', window, triggered = lambda : window.analysis.analysis(window, self, 'impulse'))]

        for a in action:
            menu.addAction(a)
        menu.exec_(window.mapToGlobal(window.event.mouse_pos))
