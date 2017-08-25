#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math
import numpy as np
import scipy.optimize

def linearFunc(x, a, b):
    return a * x+ b

class Identificate:

    # モデル式も受け取る
    def __init__(self, data, omg):
        self.data = data
        self.omg = omg
        self.amp_bode = []
        self.ang_bode = []

    def calcAmpAng(self, datum):
        #mat = []
        #for i in range(len(datum)):
        #    mat.append(datum[i])
        #mat = np.array(mat)
        #x = np.linalg.inv(mat.T.dot(mat)).dot(mat.T).dot(y)
        
        mat11 = 0
        mat12 = 0
        mat21 = 0
        mat22 = 0
        vec0 = 0
        vec1 = 0
        for i in range(len(datum)):
            mat11 += math.sin(self.omg * datum[i][0]) * math.sin(self.omg * datum[i][0])
            mat12 += math.sin(self.omg * datum[i][0]) * math.cos(self.omg * datum[i][0])
            mat21 += math.cos(self.omg * datum[i][0]) * math.sin(self.omg * datum[i][0])
            mat22 += math.cos(self.omg * datum[i][0]) * math.cos(self.omg * datum[i][0])
            vec0 += math.sin(self.omg * datum[i][0]) * datum[i][1]
            vec1 += math.cos(self.omg * datum[i][0]) * datum[i][1]

        mat = np.array([[mat11, mat12], [mat21, mat22]])
        vec = np.array([[vec0], [vec1]])
        x = np.linalg.inv(mat)
        x = x.dot(vec)
        
        amp = math.sqrt(x[0] ** 2 + x[1] ** 2)
        ang = math.atan2(x[1],x[0])
        if ang < 0:
            ang = ang + math.pi
        print('amp:{} ang:{}'.format(amp, ang))

        self.amp_bode.append([math.log10(self.omg), math.log10(amp)])
        self.ang_bode.append([math.log10(self.omg), math.log10(ang)])

    def calc(self):
        for datum in self.data:
            self.calcAmpAng(datum)
        #self.amp_bode = np.array(self.amp_bode)
        #self.ang_bode = np.array(self.ang_bode)
        self.amp_bode = np.array([[1,4], [2,8], [3,12]])
        
        ini_param = np.array([0, 0])
        param, cov = scipy.optimize.curve_fit(linearFunc, [x[0] for x in self.amp_bode], [x[1] for x in self.amp_bode], p0=ini_param)

        print('params:{} conv:{}'.format(param, cov))









po = [[0, -27.20105554446849],[1, -31.253532444644105],[2, -34.993734379677115],[3, -38.384290488179126],[4, -41.391323454282684],[5, -43.9847879985835],[6, -46.138771080640325],[7, -47.831750813509395],[8, -49.04681150332458],[9, -49.77181266531887],[10, -49.99951032753518],[11, -49.727629410199455],[12, -48.95888645756587],[13, -47.70096249510445],[14, -45.96642628323379],[15, -43.772608734421425],[16, -41.14142974843544],[17, -38.09917919595166],[18, -34.67625423885612],[19, -30.906855611851665],[20, -26.828645900021748],[21, -22.482373226730072],[22, -17.911464111841436],[23, -13.161589568290047],[24, -8.28020877241547],[25, -3.316094867560034],[26, 1.6811523610568349],[27, 6.661602070997111],[28, 11.575491255076948],[29, 16.37372195688465],[30, 21.008351841332047],[31, 25.433073218618684],[32, 29.60367573536115],[33, 33.47848810983012],[34, 37.01879449762243],[35, 40.18922132758105],[36, 42.95809074282479],[37, 45.29773711542309],[38, 47.18478347220524],[39, 48.6003750697488],[40, 49.53036778474352],[41, 49.96546943739588],[42, 49.901332635818086],[43, 49.33859821373067],[44, 48.28288882746387],[45, 46.74475277623415],[46, 44.73955860702521],[47, 42.28734155714671],[48, 39.412603368765815],[49, 36.1440674755988],[50, 32.51439200785584],[51, 28.55984348299943],[52, 24.319934442689984],[53, 19.837028656530602],[54, 15.155917837285113],[55, 10.32337409688983],[56, 5.387682614972203],[57, 0.39815918929686717],[58, -4.595342511384082],[59, -9.54292906870947],[60, -14.395165833253266],[61, -19.103570859200456],[62, -23.621099319923307],[63, -27.902613564338967],[64, -31.90533411739737],[65, -35.58926711845615],[66, -38.917603926714925],[67, -41.857088900987335],[68, -44.37835167907523],[69, -46.45620063671842],[70, -48.06987459397784],[71, -49.20325025408217],[72, -49.8450033020798],[73, -49.98872155365056],[74, -49.63296902353166],[75, -48.78130027340788],[76, -47.4422248959062],[77, -45.62912248955923],[78, -43.360108974279065],[79, -40.65785558307443],[80, -37.549362338583805],[81, -34.065688277774996],[82, -30.241641120314206],[83, -26.115429481336577],[84, -21.72828110359484],[85, -17.124030923480625],[86, -12.348683086831045],[87, -7.44995129070994],[88, -2.4767820439183708],[89, 2.521134390340561],[90, 7.493860483147617],[91, 12.39171039914799],[92, 17.16574644099477],[93, 21.768268018644658],[94, 26.15328825788482],[95, 30.276993485980054],[96, 34.09818100340678],[97, 37.57867076760741],[98, 40.68368687535527],[99, 43.38220503208336]]

iden = Identificate([po, po, po], 0.1)
iden.calc()