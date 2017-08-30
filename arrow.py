#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QAction, QMenu
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import Qt, QPoint

class ArrowManager:

    def __init__(self):
        self.arrow_list = [] # list of managing Arrow

        self.selected_obj_pos_dis = [] # Arrowモードで選択しているオブジェクト

    def push(self, w, num):
        arrow = Arrow(self.selected_obj_pos_dis, num)
        self.arrow_list.append(arrow)

    def paint(self, w, canvas):
        for a in self.arrow_list:
            a.paint(w, canvas)

    def updateObjPosDis(self, obj_pos_dis):
        self.selected_obj_pos_dis = obj_pos_dis

    def whichBlue(self):
        for a in self.arrow_list:
            if a.is_blue:
                return self.arrow_list.index(a)
        return -1


class Arrow:

    def __init__(self, obj_pos_dis, num):
        self.pos = [obj_pos_dis[1]] # すでに定まっている点群
        self.way_pos = self.pos # 選択途中の点群

        self.is_blue = False # 枠を青くするかどうか

        self.mode = 0 # -1:死 0:選択途中 1:選択終了 

        self.near_obj_pos_dis = [] # Arrowの終点とあるオブジェクトの最短位置、距離
        self.selected_obj = -1 # Arrowが選択しているオブジェクト

        self.num = num # ルンゲクッタの時に使う矢印のnum

        self.direct = -1 # 矢印の最後の向き

        self.dot_line = False # 点線を書くか

    def setMode(self, mode):
        self.mode = mode

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

    def paint(self, w, canvas):
        if self.mode == -1:
            return

        # Line
        if self.is_blue == False:
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
                self.direct_x = 0
                self.direct_y = direct_sgn
            p = []
            p.append(QPoint(self.way_pos[-1].x() - 6, self.way_pos[-1].y() - direct_sgn * 10))
            p.append(QPoint(self.way_pos[-1].x(), self.way_pos[-1].y() - direct_sgn * 1))
            p.append(QPoint(self.way_pos[-1].x() + 6, self.way_pos[-1].y() - direct_sgn * 10))
            for i in range(len(p) - 1):
                canvas.drawLine(p[i], p[i + 1])
        else:
            direct = self.way_pos[-1].x() - self.way_pos[-2].x()
            direct_sgn = direct / abs(direct)
            self.direct_x = direct_sgn
            self.direct_y = 0
            p = []
            p.append(QPoint(self.way_pos[-1].x() - direct_sgn * 10, self.way_pos[-1].y() - 6))
            p.append(QPoint(self.way_pos[-1].x() - direct_sgn * 1, self.way_pos[-1].y()))
            p.append(QPoint(self.way_pos[-1].x() - direct_sgn * 10, self.way_pos[-1].y() + 6))
            for i in range(len(p) - 1):
                canvas.drawLine(p[i], p[i + 1])

        if self.dot_line == True:
            pen = QPen(Qt.black, 2, Qt.SolidLine)
            pen.setStyle(Qt.DotLine)
            canvas.setPen(pen)
            canvas.drawLine(self.way_pos[-1].x(), 0, self.way_pos[-1].x(), 1000)
            canvas.drawLine(0, self.way_pos[-1].y(), 1000, self.way_pos[-1].y())
            self.dot_line = False

    def setFrameBlue(self, blue_or_not):
        if blue_or_not:
            self.is_blue = True
        else:
            self.is_blue = False

    def onRightClick(self, pos, w):
        menu = QMenu(w)
        action = [(QAction('Delete', w, triggered = lambda : self.setMode(-1)))]
        for a in action:
            menu.addAction(a)
        menu.exec_(w.mapToGlobal(w.event.mouse_pos))

