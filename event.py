from PyQt5.QtWidgets import * #QWidget, QPushButton, QFrame, QApplication, QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import block, math_util

class Event:
    def __init__(self):
        self.selected_block_id = -1 # 選択しているblock_id
        self.selected_arrow_id = -1 # 選択しているarrow_id

        self.arrow_pos_dis = [] # Arrowの始点とあるオブジェクトの最短位置、距離
        self.block_pos_dis = [] # Blockの始点とあるオブジェクトの最短位置、距離

        self.cursor_near_obj = -1 # カーソル選択範囲内のオブジェクト
        self.cursor_selected_obj = -1 # カーソルが選択しているオブジェクト

        self.esc_key = False

    def mousePress(self, mouse_event, widget):
        pos = mouse_event.pos()

        if widget.mode == 'Cursor':
            if self.cursor_near_obj != -1:
                self.cursor_selected_obj = self.cursor_near_obj
                self.cursor_selected_obj.setFrameBlue(True)

        if widget.mode == 'Block':
            if self.selected_block_id == -1:
                self.selected_block_id = len(widget.block_manager.block_list)
                widget.block_manager.push(widget, pos)
                print('No.' + str(self.selected_block_id) + ' Block has been born')
            elif self.selected_block_id != -1 and self.block_pos_dis != []: # オブジェクトを終点とする
        elif widget.mode == 'Arrow':
            if self.selected_arrow_id != -1 and self.arrow_pos_dis != []: # オブジェクトを終点とする
                widget.arrow_manager.arrow_list[self.selected_arrow_id].removeLatestPoint()
                widget.arrow_manager.arrow_list[self.selected_arrow_id].setWayPoint(self.arrow_pos_dis[0])
                self.selected_arrow_id = -1
                return

            if self.selected_arrow_id == -1:
                self.selected_arrow_id = len(widget.arrow_manager.arrow_list)
                widget.arrow_manager.push(widget)
                print('No.' + str(self.selected_arrow_id) + ' Arrow has been born')
            if self.arrow_pos_dis != []:
                widget.arrow_manager.arrow_list[self.selected_arrow_id].setPoint(self.arrow_pos_dis[0])
            else:
                widget.arrow_manager.arrow_list[self.selected_arrow_id].setPoint(pos)

    def mouseMove(self, mouse_event, widget):
        pos = mouse_event.pos()

        # カーソルの近くにArrow、Blockがあるか
        if widget.mode == 'Cursor' or widget.mode == 'Arrow':
            pos_all = []
            dis_all = []
            obj_all = []
            for bl in widget.block_manager.block_list:
                # カーソルとBlockの最短位置と距離
                [tmp_pos, tmp_dis] = math_util.nearestPointBlock(pos.x(), pos.y(), bl.start_x, bl.start_y, bl.end_x, bl.end_y)
                pos_all.append(tmp_pos)
                dis_all.append(tmp_dis)
                obj_all.append(bl)

            for ar in widget.arrow_manager.arrow_list:
                if widget.arrow_manager.arrow_list.index(ar) == self.selected_arrow_id:
                    continue
                # カーソルとArrowの最短位置と距離
                [tmp_pos, tmp_dis] = math_util.nearestPointArrow(pos.x(), pos.y(), ar.way_pos)
                if tmp_dis == None:
                    continue
                pos_all.append(tmp_pos)
                dis_all.append(tmp_dis)
                obj_all.append(ar)

            if pos_all == []: # 既存のオブジェクトが無い
                return

            min_dis = min(dis_all)
            min_pos = pos_all[dis_all.index(min_dis)]
            min_obj = obj_all[dis_all.index(min_dis)]
        # カーソルの近くにArrowの端点があるか
        elif widget.mode == 'Block':
            pos_all = []
            dis_all = []
            obj_all = []

            for ar in widget.arrow_manager.arrow_list:
                # Blockの二辺とArrowの端点との最短位置と距離
                b = block_manager.block_list[self.selected_block_id]
                [tmp_pos, tmp_dis] = math_util.nearestBlockArrow(b.start_x, b.start_y, b.end_x, b.end_y, pos.y(), ar.way_pos)
                if tmp_dis == None:
                    continue
                pos_all.append(tmp_pos)
                dis_all.append(tmp_dis)
                obj_all.append(ar)

            if pos_all == []: # 既存のArrowが無い
                return

            min_dis = min(dis_all)
            min_pos = pos_all[dis_all.index(min_dis)]
            min_obj = obj_all[dis_all.index(min_dis)]

        if widget.mode == 'Cursor':
            for o in obj_all:
                o.setFrameBlue(False)
            if min_dis < 6: # そのオブジェクトを選択する
                min_obj.setFrameBlue(True)
                self.arrow_pos_dis = [min_pos, min_dis]
                self.cursor_near_obj = o
            else:
                self.arrow_pos_dis = []
                self.cursor_near_obj = -1
        elif widget.mode == 'Block':
            if self.selected_block_id != -1: # あるBlockが選択されている
                for o in obj_all:
                    o.setFrameBlue(False)
                if min_dis < 6: # そのオブジェクトを選択する
                    min_obj.setFrameBlue(True)
                    p = min_pos
                    #widget.block_manager.block_list[self.selected_block_id].setEndPoint(widget, min_pos)
                else:
                    self.arrow_pos_dis = []
                if self.selected_arrow_id != -1: # あるArrowが選択されてる
                    widget.arrow_manager.arrow_list[self.selected_arrow_id].setWayPoint(pos)
        elif widget.mode == 'Arrow':
            for o in obj_all:
                o.setFrameBlue(False)
            if min_dis < 6: # そのオブジェクトを選択する
                min_obj.setFrameBlue(True)
                self.arrow_pos_dis = [min_pos, min_dis]
            else:
                self.arrow_pos_dis = []

            # TODO 下二行インデント
            if self.selected_arrow_id != -1: # あるArrowが選択されてる
                widget.arrow_manager.arrow_list[self.selected_arrow_id].setWayPoint(pos)
                    
    def mouseRelease(self, mouse_event, widget):
        pos = mouse_event.pos()

        if widget.mode == 'Block':
            if self.selected_block_id != -1:
                widget.block_manager.block_list[self.selected_block_id].showFormula(widget)
            self.selected_block_id = -1

    def keyPress(self, key_event, widget):
        if key_event.key() == Qt.Key_Escape:
            if widget.mode == 'Arrow':
                if self.selected_arrow_id != -1:
                    widget.arrow_manager.arrow_list[self.selected_arrow_id].removeLatestPoint()
                    self.selected_arrow_id = -1
