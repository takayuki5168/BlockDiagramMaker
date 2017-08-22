import math

from PyQt5.QtCore import QPoint

import block, arrow, combine

# 点と点
def disPointPoint(point1_pos, point2_pos):
    po = point1_pos - point2_pos
    return math.hypot(po.x(), po.y())

# 点と円
def nearestPointCircle(point_pos, circle_pos, radius):
    dis = disPointPoint(point_pos, circle_pos)

    po = circle_pos + (point_pos - circle_pos) * radius / dis
    return po

# 点と直線
def nearestPointLine(point_pos, line_start, line_end):
    po_x = point_pos.x()
    po_y = point_pos.y()
    li_start_x = line_start.x()
    li_start_y = line_start.y()
    li_end_x = line_end.x()
    li_end_y = line_end.y()

    if li_start_x == li_end_x: # when vertical line
        small_y = min(li_start_y, li_end_y)
        large_y = max(li_start_y, li_end_y)

        if large_y <= po_y:
            return QPoint(li_start_x, large_y)
        elif large_y > po_y and small_y < po_y:
            return QPoint(li_start_x, po_y)
        else:
            return QPoint(li_start_x, small_y)

    else: # when horizontal line
        small_x = min(li_start_x, li_end_x)
        large_x = max(li_start_x, li_end_x)

        if large_x <= po_x:
            return QPoint(large_x, li_start_y)
        elif large_x > po_x and small_x < po_x:
            return QPoint(po_x, li_start_y)
        else:
            return QPoint(small_x, li_start_y)

# 点とブロック
def nearestPointBlock(point_pos, block_start, block_end):
    po_x = point_pos.x()
    po_y = point_pos.y()
    bl_start_x = block_start.x()
    bl_start_y = block_start.y()
    bl_end_x = block_end.x()
    bl_end_y = block_end.y()

    pos = []

    pos.append(nearestPointLine(point_pos, QPoint(bl_start_x, bl_start_y), QPoint(bl_end_x, bl_start_y)))
    pos.append(nearestPointLine(point_pos, QPoint(bl_end_x, bl_start_y), QPoint(bl_end_x, bl_end_y)))
    pos.append(nearestPointLine(point_pos, QPoint(bl_start_x, bl_end_y), QPoint(bl_end_x, bl_end_y)))
    pos.append(nearestPointLine(point_pos, QPoint(bl_start_x, bl_start_y), QPoint(bl_start_x, bl_end_y)))

    dis = []
    for p in pos:
        dis.append(math.hypot(p.x() - po_x, p.y() - po_y))

    pos_dis = [pos[0], dis[0]]
    for i in range(len(pos) - 1):
        if pos_dis[1] > dis[i + 1]:
            pos_dis = [pos[i + 1], dis[i + 1]]

    return pos_dis

# 点と矢印
def nearestPointArrow(point_pos, arrow_way_pos):
    po_x = point_pos.x()
    po_y = point_pos.y()

    if len(arrow_way_pos) == 1:
        return [None, None]

    pos = []

    for i in range(len(arrow_way_pos) - 1):
        ar_pre_p = arrow_way_pos[i]
        ar_post_p = arrow_way_pos[i + 1]
        pos.append(nearestPointLine(point_pos, ar_pre_p, ar_post_p))

    dis = []
    for p in pos:
        dis.append(math.hypot(p.x() - po_x, p.y() - po_y))

    pos_dis = [pos[0], dis[0]]
    for i in range(len(pos) - 1):
        if pos_dis[1] > dis[i + 1]:
            pos_dis = [pos[i + 1], dis[i + 1]]

    return pos_dis

# ブロックと矢印
#def nearestBlockArrow(block_start, block_end, ar_way_pos):
#    bl_start_x = block_start.x()
#    bl_start_y = block_start.y()
#    bl_end_x = block_end.x()
#    bl_end_y = block_end.y()
#
#    if ar_way_pos == []:
#        return [None, None]
#    
#    pos = []
#
#    pos.append(nearestPointLine(way_pos[0], QPoint(bl_start_x, bl_end_y), QPoint(bl_end_x, bl_end_y)))
#    pos.append(nearestPointLine(way_pos[0], QPoint(bl_end_x, bl_start_y), QPoint(bl_end_x, bl_end_y)))
#    pos.append(nearestPointLine(way_pos[-1], QPoint(bl_start_x, bl_end_y), QPoint(bl_end_x, bl_end_y)))
#    pos.append(nearestPointLine(way_pos[-1], QPoint(bl_end_x, bl_start_y), QPoint(bl_end_x, bl_end_y)))
#
#    dis = []
#    for p in pos:
#        dis.append(math.hypot(p.x() - pos_x, p.y() - pos_y))
#
#    pos_dis = [pos[0], dis[0]]
#    for i in range(len(pos) - 1):
#        if pos_dis[1] > dis[i + 1]:
#            pos_dis = [pos[i + 1], dis[i + 1]]
#
#    return pos_dis

# 点と結合
def nearestPointCombine(point_pos, combine_pos, radius):
    pos = nearestPointCircle(point_pos, combine_pos, radius)
    dis = disPointPoint(pos, point_pos)
    pos_dis = [pos, dis]
    return pos_dis

def nearObjPosDis(pos, all_obj):
    pos_all = []
    dis_all = []
    obj_all = []

    # カーソルと各オブジェクトの最短位置と距離
    for o in all_obj:
        if o.mode == -1:
            continue
        if type(o) == block.Block:
            [tmp_pos, tmp_dis] = nearestPointBlock(pos, o.start_pos, o.end_pos)
        elif type(o) == arrow.Arrow:
            [tmp_pos, tmp_dis] = nearestPointArrow(pos, o.way_pos)
        elif type(o) == combine.Combine:
            [tmp_pos, tmp_dis] = nearestPointCombine(pos, o.pos, o.radius)
        pos_all.append(tmp_pos)
        dis_all.append(tmp_dis)
        obj_all.append(o)

    if pos_all == []: # 既存のオブジェクトが無い
        # self.setEndPoint(mouse_pos)
        return [None, None, None]

    # 距離が最小の時のdis, pos, objを求める
    min_dis = min(dis_all)
    min_pos = pos_all[dis_all.index(min_dis)]
    min_obj = obj_all[dis_all.index(min_dis)]


    for o in all_obj:
        # まずは全部青でなくする
        o.setFrameBlue(False)
    if min_dis < 10: # 距離が十分近かったら
        # そのオブジェクトを青にして選択する
        min_obj.setFrameBlue(True)

        return [min_obj, min_pos, min_dis]
    else:
        return [None, None, None]
