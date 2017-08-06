#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QPoint

class ArrowManager:

    def __init__(self):
        self.arrow_list = [] # Arrowを管理するリスト

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
        self.way_pos = [self.pos] # 選択途中の点群

        self.frame_blue = False # 枠を青くするかどうか

        self.mode = 0 # -1:死 0:選択途中 1:選択終了 

        self.near_obj_pos_dis = [] # Arrowの終点とあるオブジェクトの最短位置、距離
        self.selected_obj = -1 # Arrowが選択しているオブジェクト

    def setWayPoint(self, pos):
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

        #for o in all_obj:
        #    # まずは全部青でなくする
        #    o.setFrameBlue(False)
        #if min_dis < 6: # 距離が十分近かったら
        #    # そのオブジェクトを青にして選択する
        #    min_obj.setFrameBlue(True)
        #else:
        #    self.near_obj_pos_dis = []

        #self.setWayPoint(pos)

    def paint(self, widget, canvas):
        if self.mode == -1:
            return

        if self.frame_blue == False:
            canvas.setPen(QColor(0, 0, 0))
        else:
            canvas.setPen(QColor(0, 0, 255))
        for i in range(len(self.way_pos) - 1):
            canvas.drawLine(self.way_pos[i], self.way_pos[i + 1])

    def setFrameBlue(self, blue_or_not):
        if blue_or_not:
            self.frame_blue = True
        else:
            self.frame_blue = False
