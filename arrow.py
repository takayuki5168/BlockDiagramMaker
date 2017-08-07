#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QPoint

class ArrowManager:

    def __init__(self):
        self.arrow_list = [] # List of managing Arrow

        self.selected_obj_pos_dis = [] # Arrowモードで選択しているオブジェクト

    def push(self, widget):
        arrow = Arrow(self.selected_obj_pos_dis)
        self.arrow_list.append(arrow)

    def paint(self, widget, canvas):
        for a in self.arrow_list:
            a.paint(widget, canvas)

    def updateObjPosDis(self, obj_pos_dis):
        self.selected_obj_pos_dis = obj_pos_dis

class Arrow:

    def __init__(self, obj_pos_dis):
        self.pos = [obj_pos_dis[1]] # すでに定まっている点群
        self.way_pos = self.pos # 選択途中の点群

        self.frame_blue = False # 枠を青くするかどうか

        self.mode = 0 # -1:死 0:選択途中 1:選択終了 

        self.near_obj_pos_dis = [] # Arrowの終点とあるオブジェクトの最短位置、距離
        self.selected_obj = -1 # Arrowが選択しているオブジェクト

    def setWayPoint(self, near_obj_pos_dis):
        self.near_obj_pos_dis = near_obj_pos_dis
        pos = self.near_obj_pos_dis[1]
        
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
        if self.mode == -1:
            return

        # Line
        if self.frame_blue == False:
            canvas.setPen(QPen(QColor(0, 0, 0), 2))
        else:
            canvas.setPen(QPen(QColor(0, 0, 255), 2))
        for i in range(len(self.way_pos) - 1):
            canvas.drawLine(self.way_pos[i], self.way_pos[i + 1])

        # triangle
        if len(self.way_pos) == 1:
            return
        if self.way_pos[-1].x() == self.way_pos[-2].x():
            # calc direct
            direct = self.way_pos[-1].y() - self.way_pos[-2].y()
            if direct == 0:
                direct_sgn = 0
            else:
                direct_sgn = direct / abs(direct)
            p = []
            p.append(QPoint(self.way_pos[-1].x() - 6, self.way_pos[-1].y() - direct_sgn * 10))
            p.append(QPoint(self.way_pos[-1].x(), self.way_pos[-1].y() - direct_sgn * 1))
            p.append(QPoint(self.way_pos[-1].x() + 6, self.way_pos[-1].y() - direct_sgn * 10))
            for i in range(len(p) - 1):
                canvas.drawLine(p[i], p[i + 1])
        else:
            direct = self.way_pos[-1].x() - self.way_pos[-2].x()
            direct_sgn = direct / abs(direct)
            p = []
            p.append(QPoint(self.way_pos[-1].x() - direct_sgn * 10, self.way_pos[-1].y() - 6))
            p.append(QPoint(self.way_pos[-1].x() - direct_sgn * 1, self.way_pos[-1].y()))
            p.append(QPoint(self.way_pos[-1].x() - direct_sgn * 10, self.way_pos[-1].y() + 6))
            for i in range(len(p) - 1):
                canvas.drawLine(p[i], p[i + 1])

    def setFrameBlue(self, blue_or_not):
        if blue_or_not:
            self.frame_blue = True
        else:
            self.frame_blue = False
