#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import math
import os
import json
import scipy.optimize
from PyQt5.QtWidgets import QMainWindow, QDialog, QFileDialog
from PyQt5.QtWidgets import qApp

def linearFunc(x, a, b): return a * x+ b

class Identificate:

    # モデル式も受け取る
    def __init__(self):
        self.file = []

    def execute(self, w):
        # ログが入っているディレクトリの選択
        #dir_name = QFileDialog.getExistingDirectory(w, 'Open Directory', '/home/private/hobby/python-qt5')
        dir_name = '/home/takayuki/private/hobby/python-qt5'
        #json_file = open('/home/takayuki/private/hobby/python-qt5/json/format.json')
        json_file = open(dir_name + '/json/format.json')
        json_data = json.load(json_file)
        which_sample = json_data['which_use']

        sample_data = json_data[which_sample]
        self.cycle_sec = sample_data['cycle_sec']
        freqs = sample_data['freqency']
        input_data = sample_data['input']
        output_data = sample_data['output']

        # 入力値に関して
        input_time_line = int(input_data['time_line'])
        input_gain_line = int(input_data['gain_line'])
        input_phase_line = int(input_data['phase_line'])
        self.input_amp_bode = []
        self.input_ang_bode = []
        for i in range(len(freqs)):
            f = dir_name + '/' + input_data['file_name'][i]
            freq = freqs[i]

            input_datum = []
            for line in open(f):
                l = line.split(' ')
                input_datum.append([float(l[input_time_line - 1]), float(l[input_gain_line - 1])])
            self.calcAmpAng(input_datum, freq, True)
        # 出力値に関して
        output_time_line = int(output_data['time_line'])
        output_gain_line = int(output_data['gain_line'])
        output_phase_line = int(output_data['phase_line'])
        self.output_amp_bode = []
        self.output_ang_bode = []
        for i in range(len(freqs)):
            f = dir_name + '/' + output_data['file_name'][i]
            freq = freqs[i]

            output_datum = []
            for line in open(f):
                l = line.split(' ')
                output_datum.append([float(l[output_time_line - 1]), float(l[output_gain_line - 1])])
            self.calcAmpAng(output_datum, freq, False)
        #for i in self.amp_bode:
        #    print('{} {}'.format(i[0], i[1]))
        self.amp_bode = []
        self.ang_bode = []
        for i in range(len(freqs)):
            omega = math.log10(freqs[i])
            amp = 20 * math.log10(self.output_amp_bode[i])# / self.input_amp_bode[i])
            ang = self.output_ang_bode[i] - self.input_ang_bode[i]
            self.amp_bode.append([omega, amp])
            self.ang_bode.append([omega, ang])

        ini_params = np.array([0, 0])
        params, cov = scipy.optimize.curve_fit(linearFunc, [x[0] for x in self.amp_bode], [x[1] for x in self.amp_bode], p0=ini_params)
        print('params:{} conv:{}'.format(params, cov))
        print('m = {}'.format(math.pow(10, params[1] / -20.0)))

        self.plotBode(params)


    def calcAmpAng(self, datum, omg, input_or_not):
        po = 2 * math.pi * omg * self.cycle_sec # TODO 何msかでこの数字を変える
        mat11 = 0
        mat12 = 0
        mat21 = 0
        mat22 = 0
        vec0 = 0
        vec1 = 0
        for i in range(len(datum)):
            mat11 += math.sin(po * datum[i][0]) * math.sin(po * datum[i][0])
            mat12 += math.sin(po * datum[i][0]) * math.cos(po * datum[i][0])
            mat21 += math.cos(po * datum[i][0]) * math.sin(po * datum[i][0])
            mat22 += math.cos(po * datum[i][0]) * math.cos(po * datum[i][0])
            vec0 += math.sin(po * datum[i][0]) * datum[i][1]
            vec1 += math.cos(po * datum[i][0]) * datum[i][1]

        mat = np.array([[mat11, mat12], [mat21, mat22]])
        vec = np.array([[vec0], [vec1]])
        x = np.linalg.inv(mat)
        x = x.dot(vec)
        
        amp = math.sqrt(x[0] ** 2 + x[1] ** 2)
        ang = math.atan2(x[1],x[0])
        #if ang < 0:
        #    ang = ang + math.pi
        print('amp:{} ang:{}'.format(amp, ang))

        if input_or_not == True:
            self.input_amp_bode.append(amp)
            self.input_ang_bode.append(ang)
        else:
            self.output_amp_bode.append(amp)
            self.output_ang_bode.append(ang)

        #self.plotSin([d[0] for d in datum], [d[1] for d in datum], 'time[s]', 'output', omg, amp, ang, input_or_not)

    def plotSin(self, x_val, y_val, x_label, y_label, omg, amp, ang, input_or_not):
        po = 2 * math.pi * omg * self.cycle_sec # TODO

        ax1 = plt.subplot(1,1,1)
        ax1.scatter(x_val, y_val, color = 'g', s = 0.5)#, marker = ".", markersize = 0.1)
        y_real = [amp * math.sin(po * x + ang) for x in x_val]
        ax1.plot(x_val, y_real, 'b-')

        if input_or_not == True:
            ax1.set_title('Input Omega = {}'.format(omg))
        else:
            ax1.set_title('Output Omega = {}'.format(omg))
        ax1.set_xlabel(x_label)   # 1番目にxラベルを追加
        ax1.set_ylabel(y_label)   # 1番目にyラベルを追加

        plt.show()

    def plotBode(self, params):
        ax1 = plt.subplot(2, 1, 1)
        ax1.set_title('Bode')
        ax1.set_xlabel('omega')
        ax1.set_ylabel('gain')

        ax1.scatter([x[0] for x in self.amp_bode], [x[1] for x in self.amp_bode], color = 'g')
        y_real = [params[0] * x[0] + params[1] for x in self.amp_bode]
        ax1.plot([x[0] for x in self.amp_bode], y_real, 'b-')

        ax2 = plt.subplot(2, 1, 2)
        ax2.set_xlabel('omega')
        ax2.set_ylabel('phase')

        ax2.scatter([x[0] for x in self.ang_bode], [x[1] for x in self.ang_bode], color = 'g')

        self.amp_bode
        plt.show()
