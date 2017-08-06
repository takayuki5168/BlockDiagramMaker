from PyQt5.QtWidgets import * #QWidget, QPushButton, QFrame, QApplication, QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import math_util

class Event:
    def __init__(self):
        self.selected_block_id = -1 # 選択しているblock_id
        self.selected_arrow_id = -1 # 選択しているarrow_id

        self.cursor_near_obj = -1 # カーソル、Arrowの選択範囲可能のオブジェクト
        self.cursor_selected_obj = -1 # カーソル、Arrowが選択しているオブジェクト

    def mousePress(self, mouse_event, widget):
        pos = mouse_event.pos()

        #if widget.operate_mode == 'Cursor':
        #    if self.cursor_near_obj != -1:
        #        self.cursor_selected_obj = self.cursor_near_obj
        #        self.cursor_selected_obj.setFrameBlue(True)

        if widget.operate_mode == 'Block':
            if self.selected_block_id == -1:
                # create new Block
                self.selected_block_id = len(widget.block_manager.block_list)
                widget.block_manager.push(widget, pos)
                print('No.' + str(self.selected_block_id) + ' Block has been born')
            #elif self.selected_block_id != -1 and self.block_pos_dis != []: # オブジェクトを終点とする
        elif widget.operate_mode == 'Arrow':
            if self.selected_arrow_id == -1:
                # create new Arrow
                self.selected_arrow_id = len(widget.arrow_manager.arrow_list)
                widget.arrow_manager.push(widget)
                print('No.' + str(self.selected_arrow_id) + ' Arrow has been born')
            else:
                ar = widget.arrow_manager.arrow_list[self.selected_arrow_id]
                if ar.near_obj_pos_dis != []:
                    # そのオブジェクトを終端とする
                    ar.removeLatestPoint()
                    ar.setWayPoint(ar.near_obj_pos_dis[1])
                else:
                    # マウスを終端とする
                    ar.setPoint(pos)

    def mouseMove(self, mouse_event, widget):
        pos = mouse_event.pos()

        #if widget.operate_mode == 'Cursor':
        #    all_obj = arrow_manager.arrow_list + block_manager.block_list
        if widget.operate_mode == 'Arrow':
            if self.selected_arrow_id != -1:
                ar = widget.arrow_manager.arrow_list[self.selected_arrow_id]
                # 自分以外のArrow + Block
                all_obj = widget.arrow_manager.arrow_list[:self.selected_arrow_id] + widget.arrow_manager.arrow_list[self.selected_arrow_id + 1:] + widget.block_manager.block_list
                near_obj_pos_dis = math_util.nearObjPosDis(pos, all_obj)
                if near_obj_pos_dis != []:
                    ar.setWayPoint(near_obj_pos_dis[1])
                else:
                    ar.setWayPoint(pos)
            else:
                all_obj = widget.arrow_manager.arrow_list + widget.block_manager.block_list
                near_obj_pos_dis = math_util.nearObjPosDis(pos, all_obj)
                if near_obj_pos_dis != []:
                    widget.arrow_manager.updateObjPosDis(near_obj_pos_dis)
                else:
                    widget.arrow_manager.updateObjPosDis([None, pos, None])
        elif widget.operate_mode == 'Block':
            if self.selected_block_id != -1:
                bl = widget.block_manager.block_list[self.selected_block_id]

                # judge only with Arrow
                all_obj = widget.arrow_manager.arrow_list
                near_obj_pos_dis = math_util.nearObjPosDis(pos, all_obj)
                if near_obj_pos_dis == []:
                    bl.setEndPoint(pos)
                else:
                    bl.setEndPoint(near_obj_pos_dis[1])

        #if widget.operate_mode == 'Cursor':
        #    for o in obj_all:
        #        o.setFrameBlue(False)
        #    if min_dis < 6: # そのオブジェクトを選択する
        #        min_obj.setFrameBlue(True)
        #        self.arrow_pos_dis = [min_pos, min_dis]
        #        self.cursor_near_obj = o
        #    else:
        #        self.arrow_pos_dis = []
        #        self.cursor_near_obj = -1
                    
    def mouseRelease(self, mouse_event, widget):
        pos = mouse_event.pos()

        if widget.operate_mode == 'Block':
            if self.selected_block_id != -1:
                widget.block_manager.block_list[self.selected_block_id].showFormula(widget)
            self.selected_block_id = -1

    def keyPress(self, key_event, widget):
        if key_event.key() == Qt.Key_Escape:
            if widget.operate_mode == 'Arrow':
                if self.selected_arrow_id != -1:
                    widget.arrow_manager.arrow_list[self.selected_arrow_id].removeLatestPoint()
                    self.selected_arrow_id = -1
