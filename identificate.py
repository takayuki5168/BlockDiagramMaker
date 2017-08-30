#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import math
import os
import json
import scipy.optimize
from PyQt5.QtWidgets import QFileDialog

def linearFunc(x, a, b): return a * x+ b

class Identificate:

    # モデル式も受け取る
    def __init__(self):
        self.amp_bode = []
        self.ang_bode = []
        self.file = []

    def execute(self, w):
        # ログが入っているディレクトリの選択
        #dir_name = QFileDialog.getExistingDirectory(w, 'Open Directory', '/home/private/hobby/python-qt5')
        dir_name = '/home/takayuki/private/hobby/python-qt5'
        #json_file = open('/home/takayuki/private/hobby/python-qt5/json/format.json')
        json_file = open(dir_name + '/json/format.json')
        json_data = json.load(json_file)
        sample = json_data['which_use']
        gain = json_data[sample]['gain']
        phase = json_data[sample]['phase']

        time_line = int(gain['time_line'])
        gain_line = int(gain['gain_line'])
        for i in range(len(gain['file_name'])):
            f = dir_name + '/' + gain['file_name'][i]
            freq = gain['freqency'][i]

            datum = []
            for line in open(f):
                l = line.split(' ')
                datum.append([float(l[time_line - 1]), float(l[gain_line - 1])])
            self.calcAmpAng(datum, freq)
        for i in self.amp_bode:
            print('{} {}'.format(i[0], i[1]))

        ini_param = np.array([0, 0])
        param, cov = scipy.optimize.curve_fit(linearFunc, [x[0] for x in self.amp_bode], [x[1] for x in self.amp_bode], p0=ini_param)
        print('params:{} conv:{}'.format(param, cov))

    def calcAmpAng(self, datum, omg):
        po = 2 * math.pi * omg * 0.001
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
        if ang < 0:
            ang = ang + math.pi
        print('amp:{} ang:{}'.format(amp, ang))

        self.amp_bode.append([math.log10(po), math.log10(amp)])
        self.ang_bode.append([math.log10(po), math.log10(ang)])
