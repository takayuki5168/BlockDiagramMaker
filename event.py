from PyQt5.QtWidgets import * #Qwindow, QPushButton, QFrame, QApplication, QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import arrow, block, combine, math_util

class Event:
    def __init__(self):
        self.selected_block_id = -1 # 作成中のblock_id
        self.selected_arrow_id = -1 # 作成中のarrow_id
        self.selected_combine_id = -1 # 作成中のcombine_id

        self.cursor_near_obj = -1 # カーソル、Arrowの選択範囲可能のオブジェクト
        self.cursor_selected_obj = -1 # カーソル、Arrowが選択しているオブジェクト

    def mousePress(self, mouse_event, window):
        self.mouse_pos = mouse_event.pos()

        if mouse_event.buttons() == Qt.RightButton: # when RightClick
            block_blue = window.block_manager.whichBlue()
            if block_blue != -1:
                window.block_manager.block_list[block_blue].onRightClick(self.mouse_pos, window)
            elif self.selected_arrow_id != -1:
                window.arrow_manager.arrow_list[self.selected_arrow_id].onRightClick(self.mouse_pos)
            elif self.selected_combine_id != -1:
                window.combine_manager.combine_list[self.selected_combine_id].onRightClick(self.mouse_pos)
        if mouse_event.buttons() == Qt.LeftButton: # when LeftClick
            if window.operate_mode == 'Block':
                if self.selected_block_id == -1: # create new Block
                    self.selected_block_id = len(window.block_manager.block_list)
                    window.block_manager.push(window, self.mouse_pos)
                    print('No.' + str(self.selected_block_id) + ' Block has been born')
                    window.block_manager.block_list[self.selected_block_id].mode = 0
                else:
                    if window.block_manager.block_list[self.selected_block_id].mode == 0:
                        bl = window.block_manager.block_list[self.selected_block_id]
                        bl.showFormula(window)
                        self.selected_block_id = -1
                        
            elif window.operate_mode == 'Arrow':
                if self.selected_arrow_id == -1: # create new Arrow
                    self.selected_arrow_id = len(window.arrow_manager.arrow_list)

                    obj_pos_dis = window.arrow_manager.selected_obj_pos_dis
                    if obj_pos_dis[0] != None: # 始点がオブジェクト
                        if type(obj_pos_dis[0]) == arrow.Arrow: # 始点がArrowのとき
                            window.arrow_manager.push(window, obj_pos_dis[0].num)
                        elif type(obj_pos_dis[0]) == combine.Combine: # 始点がCombineのとき
                            obj_pos_dis[0].output.append(self.selected_arrow_id)
                            window.arrow_manager.push(window, self.selected_arrow_id)
                        elif type(obj_pos_dis[0]) == block.Block: # 始点がBlockのとき
                            obj_pos_dis[0].output.append(self.selected_arrow_id)
                            window.arrow_manager.push(window, self.selected_arrow_id)
                    else:
                        window.arrow_manager.push(window, self.selected_arrow_id)
                    print('No.' + str(self.selected_arrow_id) + ' Arrow has been born')
                else:
                    ar = window.arrow_manager.arrow_list[self.selected_arrow_id]
                    if ar.near_obj_pos_dis[0] != None: # 端点がオブジェクトであり終点
                        obj = ar.near_obj_pos_dis[0]
                        if type(obj) == combine.Combine:
                            obj.input.append(ar.num)
                        elif type(obj) == block.Block:
                            obj.input.append(ar.num)
                        self.selected_arrow_id = -1
                    else:
                        ar.setPoint(self.mouse_pos)

            elif window.operate_mode == 'Combine':
                if self.selected_combine_id == -1:
                    # create new Combine
                    self.selected_combine_id = len(window.combine_manager.combine_list)
                    window.combine_manager.push(window, self.mouse_pos)
                    print('No.' + str(self.selected_combine_id) + ' Combine has been born')
                    self.selected_combine_id = -1

    def mouseMove(self, mouse_event, window):
       # print(self.selected_block_id)
        self.mouse_pos = mouse_event.pos()

        #if window.operate_mode == 'Cursor':
        #    all_obj = arrow_manager.arrow_list + block_manager.block_list
        if window.operate_mode == 'Arrow':
            if self.selected_arrow_id != -1:
                ar = window.arrow_manager.arrow_list[self.selected_arrow_id]
                # judge with Block and Combine
                all_obj = window.block_manager.block_list + window.combine_manager.combine_list

                # TODO posをカーソルの位置ではなく矢印の終端にする
                near_obj_pos_dis = math_util.nearObjPosDis(self.mouse_pos, all_obj)
                if near_obj_pos_dis[0] != None:
                    ar.setWayPoint(near_obj_pos_dis)
                else:
                    ar.setWayPoint([None, self.mouse_pos, None])
            else:
                all_obj = window.arrow_manager.arrow_list + window.block_manager.block_list + window.combine_manager.combine_list
                near_obj_pos_dis = math_util.nearObjPosDis(self.mouse_pos, all_obj)
                if near_obj_pos_dis[0] != None:
                    window.arrow_manager.updateObjPosDis(near_obj_pos_dis)
                else:
                    window.arrow_manager.updateObjPosDis([None, self.mouse_pos, None])

        elif window.operate_mode == 'Block':
            if self.selected_block_id != -1:
                bl = window.block_manager.block_list[self.selected_block_id]
                dis = math_util.disPointPoint(self.mouse_pos, bl.start_pos)
                if dis > 10:
                    bl.mode = 1

                bl.setEndPoint(self.mouse_pos)

    def mouseRelease(self, mouse_event, window):
        self.mousepos = mouse_event.pos()

        if window.operate_mode == 'Block':
            if self.selected_block_id != -1:
                bl = window.block_manager.block_list[self.selected_block_id]
                if bl.mode == 1:
                    bl.showFormula(window)
                    self.selected_block_id = -1

    def keyPress(self, key_event, window):
        if key_event.key() == Qt.Key_Escape:
            if window.operate_mode == 'Arrow':
                if self.selected_arrow_id != -1:
                    ar = window.arrow_manager.arrow_list[self.selected_arrow_id]
                    ar.removeLatestPoint()
                    if len(ar.pos) == 1:
                        ar.mode = -1
                    self.selected_arrow_id = -1
        if key_event.key() == Qt.Key_Delete:
            print('Block')
            for b in window.block_manager.block_list:
                print(b.input)
                print(b.output)
            print('Combine')
            for c in window.combine_manager.combine_list:
                print(c.input)
                print(c.output)
