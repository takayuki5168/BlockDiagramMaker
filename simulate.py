#!/usr/bin/python3
# -*- coding: utf-8 -*-

import arrow, block, combine

def addList(arrow_list, num_list):
    arrow_sum = 0
    for i in num_list:
        arrow_sum += arrow_list[num_list]
    return arrow_sum

def product(arrow_list, num_list):
    num_list = [int(x) for x in num_list]
    arrow_sum = 0

    if type(arrow_list) == list:
        for i in range(len(num_list)):
            arrow_sum += arrow_list[i] * num_list[i]
    else:
        arrow_sum = arrow_list * num_list[0]
    return arrow_sum

def po(num_list):
    num_list = [int(x) for x in num_list]
    po =  []

    for i in range(len(num_list) - 1):
        po.append(-num_list[len(num_list) - i - 2] / num_list[-1])
    return po

def rungekutta(state, now_time, step_time, func):
    k1 = func(state, now_time)
    k2 = func(state + step_time / 2 * k1, now_time + step_time / 2)
    k3 = func(state + step_time / 2 * k2, now_time + step_time / 2)
    k4 = func(state + step_time * k3, now_time + step_time)

    state += step_time / 6 * (k1 + 2 * k2 + 2 * k3 + k4);
    return state

class Simulate:

    def __init__(self):
        self.now_time = 0
        self.end_time = 10
        self.step_time = 0.1

    def initArrowFunc(self, widget):
        # 矢印の値、ルンゲクッタの関数
        self.arrow = [[], []]
        self.arrow_ = []
        self.func = []
        for i in range(len(widget.arrow_manager.arrow_list)):
            self.arrow[0].append(0)
            self.arrow[1].append([])
            self.func.append([])
        print(self.arrow[0])
        print(self.arrow[1])
        print(self.func)

        # Block
        for b in widget.block_manager.block_list:
            n = b.nume_coef
            d = b.deno_coef
            print('deno:{} nume:{}'.format(d, n))

            # self.arrow[1]のリスト要素確保
            if len(d) == 1:
                self.arrow[1][int(b.output[0])].append(0)
            else:
                for i in range(len(d)):
                    self.arrow[1][int(b.output[0])].append(0)

            # 関数のリスト要素確保
            if len(d) == 0:
                self.func[int(b.output[0])].append([])
            elif len(d) == 1:
                self.func[int(b.output[0])].append([])
                self.func[int(b.output[0])].append([])
            else:
                for i in range(len(d)):
                    self.func[int(b.output[0])].append([])
            print(self.func)

            # 入力部
            self.func[0].append([])
            self.func[int(0)][0] = [False, lambda arrow, time : 1]
            self.arrow[0][0] = 1

            # 関数の値初期化
            if len(d) == 0:
                self.func[int(b.output[0])][0] = [False, lambda arrow, time : product(arrow[0][int(b.input)], n)] # 仲介変数を用いない分子の計算
            else:
                self.func[int(b.output[0])][0] = [False, lambda arrow, time : product(arrow[1][int(b.output[0])], n)] # 仲介変数を用いた分子の計算

            if len(d) == 1:
                self.func[int(b.output[0])][1] = [False, lambda arrow, time : arrow[0][int(b.input[0])] / int(d[-1])]
            elif len(d) != 0:
                for i in range(len(d) - 1):
                    if i == len(d) - 1:
                        self.func[int(b.output[0])][i + 1] = [True, lambda arrow, time : product(arrow[1][int(b.output[0])], po(d)) + arrow[0][int(b.input[0])]]
                    else:
                        self.func[int(b.output[0])][i + 1] = [True, lambda arrow, time : arrow[1][int(b.output[0])][i + 1]]

        # Combine
        for c in widget.combine_manager.combine_list:
            for o in c.output:
                self.func[o][0] = [False, lambda arrow, time : addList(arrow, int(c.input[0]))]
        print('self.arrow[0] {}'.format(self.arrow[0]))
        print('self.arrow[1] {}'.format(self.arrow[1]))
        print('self.func {}'.format(self.func))

    def updateArrowFunc(self, widget):
        now_time = 0
        step_time = 0.1
        end_time = 5
        while(now_time < end_time):
            now_time += step_time
            print('now_time:{} self.arrow[0][0]:{} self.arrow[0][1]:{}'.format(now_time, self.arrow[0][0], self.arrow[0][1]))
            for i in range(len(self.arrow)):
                for j in range(len(self.func[i])):
                    if len(self.func[i]) == 1: # 関数が１つしか無いとき
                        self.arrow[0][i] = self.func[i][j][1](self.arrow, now_time)
                    else:
                        k = len(self.func[i]) - j - 1
                        if k == 0:
                            if self.func[i][k][0] == False:
                                print('a')
                                self.arrow[0][i] = self.func[i][k][1](self.arrow, now_time)
                            else:
                                print('i')
                        else:
                            if self.func[i][k][0] == False:
                                print('u')
                                self.arrow[1][i] = self.func[i][k][1](self.arrow, now_time)
                            else:
                                print('e')
                                print('{} {}'.format(i, k))
                                self.arrow[1][i][k] = rungekutta(self.arrow[1][i][k], now_time, step_time, self.func[i][k][1])
                                self.arrow[1][i][k] = rungekutta(self.arrow[1][i][k], now_time, step_time, self.func[i][k][1])








