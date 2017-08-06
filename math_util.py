import math

from PyQt5.QtWidgets import * #QWidget, QPushButton, QFrame, QApplication, QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import QPoint

# 点と直線
def nearestPointLine(point_x, point_y, line_start_x, line_start_y, line_end_x, line_end_y):
    if line_start_x == line_end_x: # when vertical line
        small_y = min(line_start_y, line_end_y)
        large_y = max(line_start_y, line_end_y)

        if large_y <= point_y:
            return QPoint(line_start_x, large_y)
        elif large_y > point_y or small_y < point_y:
            return QPoint(line_start_x, point_y)
        else:
            return QPoint(line_start_x, small_y)

    else: # when horizontal line
        small_x = min(line_start_x, line_end_x)
        large_x = max(line_start_x, line_end_x)

        if large_x <= point_x:
            return QPoint(large_x, line_start_y)
        elif large_x > point_x or small_x < point_x:
            return QPoint(point_x, line_start_y)
        else:
            return QPoint(small_x, line_start_y)

# 点とブロック
def nearestPointBlock(point_x, point_y, block_start_x, block_start_y, block_end_x, block_end_y):
    pos = []

    pos.append(nearestPointLine(point_x, point_y, block_start_x, block_start_y, block_end_x, block_start_y))
    pos.append(nearestPointLine(point_x, point_y, block_end_x, block_start_y, block_end_x, block_end_y))
    pos.append(nearestPointLine(point_x, point_y, block_start_x, block_end_y, block_end_x, block_end_y))
    pos.append(nearestPointLine(point_x, point_y, block_start_x, block_start_y, block_start_x, block_end_y))

    dis = []
    for p in pos:
        dis.append(math.hypot(p.x() - point_x, p.y() - point_y))

    pos_dis = [pos[0], dis[0]]
    for i in range(len(pos) - 1):
        if pos_dis[1] > dis[i + 1]:
            pos_dis = [pos[i + 1], dis[i + 1]]

    return pos_dis

# 点と矢印
def nearestPointArrow(point_x, point_y, way_pos):
    if way_pos == []:
        return [None, None]

    pos = []

    for i in range(len(way_pos) - 1):
        pos.append(nearestPointLine(point_x, point_y, way_pos[i].x(), way_pos[i].y(), way_pos[i + 1].x(), way_pos[i + 1].y()))

    dis = []
    for p in pos:
        dis.append(math.hypot(p.x() - point_x, p.y() - point_y))

    pos_dis = [pos[0], dis[0]]
    for i in range(len(pos) - 1):
        if pos_dis[1] > dis[i + 1]:
            pos_dis = [pos[i + 1], dis[i + 1]]

    return pos_dis

# ブロックと矢印
def nearestBlockArrow(block_start_x, block_start_y, block_end_x, block_end_y, way_pos):
    if way_pos == []:
        return [None, None]
    
    pos = []

    pos.append(nearestPointLine(point_x, point_y, way_pos[0].x(), way_pos[0].y(), block_start_x, block_end_y, block_end_x, block_end_y))
    pos.append(nearestPointLine(point_x, point_y, way_pos[0].x(), way_pos[0].y(), block_end_x, block_start_y, block_end_x, block_end_y))
    pos.append(nearestPointLine(point_x, point_y, way_pos[-1].x(), way_pos[-1].y(), block_start_x, block_end_y, block_end_x, block_end_y))
    pos.append(nearestPointLine(point_x, point_y, way_pos[-1].x(), way_pos[-1].y(), block_end_x, block_start_y, block_end_x, block_end_y))

    dis = []
    for p in pos:
        dis.append(math.hypot(p.x() - point_x, p.y() - point_y))

    pos_dis = [pos[0], dis[0]]
    for i in range(len(pos) - 1):
        if pos_dis[1] > dis[i + 1]:
            pos_dis = [pos[i + 1], dis[i + 1]]

    return pos_dis
