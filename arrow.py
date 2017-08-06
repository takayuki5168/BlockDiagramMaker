#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QPoint

import event 

class ArrowManager:

    def __init__(self):
        self.arrow_list = [] # Arrowを管理するリスト

    def push(self, widget):
        arrow = Arrow()
        self.arrow_list.append(arrow)

    def paint(self, widget, canvas):
        for a in self.arrow_list:
            a.paint(widget, canvas)

class Arrow:

    def __init__(self):
        self.pos = [] # すでに定まっている点群
        self.way_pos = [] # 選択途中の点群

        self.frame_blue = False

    def setWayPoint(self, pos):
        if self.pos == []:
            self.way_pos = [pos]
        else:
            past_pos = self.pos[-1]
            pos_diff = past_pos - pos
            if abs(pos_diff.x()) > abs(pos_diff.y()):
                self.way_pos = self.pos + [QPoint(pos.x(), past_pos.y())]
            else:
                self.way_pos = self.pos + [QPoint(past_pos.x(), pos.y())]

    def setPoint(self, pos):
        if self.pos == []:
            self.pos.append(pos)
        else:
            past_pos = self.pos[-1]
            pos_diff = past_pos - pos
            if abs(pos_diff.x()) > abs(pos_diff.y()):
                self.pos.append(QPoint(pos.x(), past_pos.y()))
            else:
                self.pos.append(QPoint(past_pos.x(), pos.y()))

    def removeLatestPoint(self):
        self.way_pos = self.way_pos[:-1]

    def paint(self, widget, canvas):
        if not self.is_alive:
            return

        if self.frame_blue == False:
            canvas.setPen(QColor(0, 0, 0))
        else:
            canvas.setPen(QColor(0, 0, 255))
        # canvas.setBrush(QColor(150, 150, 150))
        for i in range(len(self.way_pos) - 1):
            canvas.drawLine(self.way_pos[i], self.way_pos[i + 1])

    def setFrameBlue(self, blue_or_not):
        if blue_or_not:
            self.frame_blue = True
        else:
            self.frame_blue = False
