#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtGui import QPen, QColor

import event

class CombineManager:

    def __init__(self):
        self.combine_list = [] # list of managing Combine

    def push(self, window, pos):
        combine = Combine(pos)
        self.combine_list.append(combine)

    def paint(self, window, canvas):
        for c in self.combine_list:
            c.paint(window, canvas)

class Combine:

    def __init__(self, pos):
        self.radius = 15 / 2.0
        self.pos = pos

        self.is_blue = False # 枠を青くするかどうか

        self.mode = 0 # -1:死 0:選択開始(選択途中) 1:選択途中

        self.near_obj_pos_dis = [] # Blockの二辺とあるオブジェクトとその最短位置、距離
        self.selected_obj = -1 # Blockが選択しているオブジェクト

        self.input = []
        self.output = []

    def paint(self, window, canvas):
        if self.mode == -1:
            return

        if self.is_blue == False:
            canvas.setPen(QPen(QColor(0, 0, 0), 2))
        else:
            canvas.setPen(QPen(QColor(0, 0, 255), 2))

        canvas.drawArc(self.pos.x() - self.radius, self.pos.y() - self.radius, self.radius * 2, self.radius * 2, 0, 16*360);

    def setFrameBlue(self, blue_or_not):
        if blue_or_not:
            self.is_blue = True
        else:
            self.is_blue = False
