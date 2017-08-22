from PyQt5.QtWidgets import * #Qw, QPushButton, QFrame, QApplication, QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import arrow, block, combine, math_util

class Event:
    def __init__(self):
        self.latest_block_id = -1 # 作成中のblock_id
        self.latest_arrow_id = -1 # 作成中のarrow_id
        self.latest_combine_id = -1 # 作成中のcombine_id

        # カーソル、Arrowの選択範囲可能のオブジェクト
        self.cursor_near_obj_pos_dis = [None, None, None] 
        # カーソル、Arrowが選択しているオブジェクト
        self.cursor_selected_obj_pos_dis = [None, None, None] 

    def mousePress(self, mouse_event, w):
        self.mouse_pos = mouse_event.pos()

        if mouse_event.buttons() == Qt.RightButton: # when RightClick
            block_blue = w.block_manager.whichBlue()
            if block_blue != -1:
                w.block_manager.block_list[block_blue].onRightClick(self.mouse_pos, w)
            elif self.latest_arrow_id != -1:
                w.arrow_manager.arrow_list[self.latest_arrow_id].onRightClick(self.mouse_pos)
            elif self.latest_combine_id != -1:
                w.combine_manager.combine_list[self.latest_combine_id].onRightClick(self.mouse_pos)

        if mouse_event.buttons() == Qt.LeftButton: # when LeftClick
            if w.operate_mode == 'Cursor':
                if self.cursor_near_obj_pos_dis[0] != None:
                    self.cursor_selected_obj_pos_dis = self.cursor_near_obj_pos_dis
                    self.cursor_selected_obj_pos_dis[0].setFrameBlue(True)
                    print(self.cursor_selected_obj_pos_dis[0].is_blue)
                else:
                    self.cursor_selected_obj_pos_dis[0].setFrameBlue(False)
                    self.cursor_selected_obj_pos_dis[0] = None
            elif w.operate_mode == 'Block':
                if self.latest_block_id == -1: # create new Block
                    self.latest_block_id = len(w.block_manager.block_list)
                    w.block_manager.push(w, self.mouse_pos)
                    print('No.' + str(self.latest_block_id) + ' Block has been born')
                    w.block_manager.block_list[self.latest_block_id].mode = 0
                else:
                    if w.block_manager.block_list[self.latest_block_id].mode == 0:
                        bl = w.block_manager.block_list[self.latest_block_id]
                        bl.showFormula(w)
                        self.latest_block_id = -1
                        
            elif w.operate_mode == 'Arrow':
                if self.latest_arrow_id == -1: # create new Arrow
                    self.latest_arrow_id = len(w.arrow_manager.arrow_list)

                    obj_pos_dis = w.arrow_manager.selected_obj_pos_dis
                    if obj_pos_dis[0] != None: # 始点がオブジェクト
                        if type(obj_pos_dis[0]) == arrow.Arrow: # 始点がArrowのとき
                            w.arrow_manager.push(w, obj_pos_dis[0].num)
                        elif type(obj_pos_dis[0]) == combine.Combine: # 始点がCombineのとき
                            obj_pos_dis[0].output.append(self.latest_arrow_id)
                            w.arrow_manager.push(w, self.latest_arrow_id)
                        elif type(obj_pos_dis[0]) == block.Block: # 始点がBlockのとき
                            obj_pos_dis[0].output.append(self.latest_arrow_id)
                            w.arrow_manager.push(w, self.latest_arrow_id)
                    else:
                        w.arrow_manager.push(w, self.latest_arrow_id)
                    print('No.' + str(self.latest_arrow_id) + ' Arrow has been born')
                else:
                    ar = w.arrow_manager.arrow_list[self.latest_arrow_id]
                    if ar.near_obj_pos_dis[0] != None: # 端点がオブジェクトであり終点
                        obj = ar.near_obj_pos_dis[0]
                        if type(obj) == combine.Combine:
                            obj.input.append(ar.num)
                        elif type(obj) == block.Block:
                            obj.input.append(ar.num)
                        self.latest_arrow_id = -1
                    else:
                        ar.setPoint(self.mouse_pos)

            elif w.operate_mode == 'Combine':
                if self.latest_combine_id == -1:
                    # create new Combine
                    self.latest_combine_id = len(w.combine_manager.combine_list)
                    w.combine_manager.push(w, self.mouse_pos)
                    print('No.' + str(self.latest_combine_id) + ' Combine has been born')
                    self.latest_combine_id = -1

    def mouseMove(self, mouse_event, w):
        self.mouse_pos = mouse_event.pos()

        if w.operate_mode == 'Cursor':
            all_obj = w.arrow_manager.arrow_list + w.block_manager.block_list + w.combine_manager.combine_list
            near_obj_pos_dis = math_util.nearObjPosDis(self.mouse_pos, all_obj, self.cursor_selected_obj_pos_dis[0] == None)
            if near_obj_pos_dis[0] != None:
                self.cursor_near_obj_pos_dis = near_obj_pos_dis
            else:
                self.cursor_near_obj_pos_dis = [None, self.mouse_pos, None]

        else: # カーソルモードじゃなかったらカーソルモードで青くはならない
            if self.cursor_selected_obj_pos_dis[0] != None:
                self.cursor_selected_obj_pos_dis[0].setFrameBlue(False)
                self.cursor_selected_obj_pos_dis = [None, self.mouse_pos, None]
        if w.operate_mode == 'Arrow':
            if self.latest_arrow_id != -1:
                ar = w.arrow_manager.arrow_list[self.latest_arrow_id]
                # judge with Block and Combine
                all_obj = w.block_manager.block_list + w.combine_manager.combine_list

                # TODO posをカーソルの位置ではなく矢印の終端にする
                near_obj_pos_dis = math_util.nearObjPosDis(self.mouse_pos, all_obj, True)
                if near_obj_pos_dis[0] != None:
                    ar.setWayPoint(near_obj_pos_dis)
                else:
                    ar.setWayPoint([None, self.mouse_pos, None])
            else:
                all_obj = w.arrow_manager.arrow_list + w.block_manager.block_list + w.combine_manager.combine_list
                near_obj_pos_dis = math_util.nearObjPosDis(self.mouse_pos, all_obj, True)
                if near_obj_pos_dis[0] != None:
                    w.arrow_manager.updateObjPosDis(near_obj_pos_dis)
                else:
                    w.arrow_manager.updateObjPosDis([None, self.mouse_pos, None])

        elif w.operate_mode == 'Block':
            if self.latest_block_id != -1:
                bl = w.block_manager.block_list[self.latest_block_id]
                dis = math_util.disPointPoint(self.mouse_pos, bl.start_pos)
                if dis > 10:
                    bl.mode = 1

                bl.setEndPoint(self.mouse_pos)

    def mouseRelease(self, mouse_event, w):
        self.mousepos = mouse_event.pos()

        if w.operate_mode == 'Block':
            if self.latest_block_id != -1:
                bl = w.block_manager.block_list[self.latest_block_id]
                if bl.mode == 1:
                    bl.showFormula(w)
                    self.latest_block_id = -1

    def keyPress(self, key_event, w):
        if key_event.key() == Qt.Key_Escape:
            if w.operate_mode == 'Arrow':
                if self.latest_arrow_id != -1:
                    ar = w.arrow_manager.arrow_list[self.latest_arrow_id]
                    ar.removeLatestPoint()
                    if len(ar.pos) == 1:
                        ar.mode = -1
                    self.latest_arrow_id = -1
        if key_event.key() == Qt.Key_Delete:
            print('Block')
            for b in w.block_manager.block_list:
                print(b.input)
                print(b.output)
            print('Combine')
            for c in w.combine_manager.combine_list:
                print(c.input)
                print(c.output)
